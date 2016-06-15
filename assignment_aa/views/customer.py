from pyramid.view import view_config, view_defaults
from colander import Invalid

from sqlalchemy import exc

import transaction

from ..models import Customer, CustomerSchema, CusConst
from .. import events


class ValidationFailure(Exception):
    def __init__(self, errors):
        self.errors = errors


class DatabaseFailure(Exception):
    def __init__(self, msg):
        self.msg = msg


@view_defaults(route_name='customer_form')
class CustomerFormView(object):
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession
        self.notify = self.request.registry.notify
        self.schema = CustomerSchema()
        self.model = Customer

    @view_config(request_method='GET', renderer='../templates/customer.jinja2')
    def customer_form(self):
        return {'const': CusConst}

    @view_config(request_method='POST', renderer='json')
    def customer_form_save(self):
        # validate and save
        vdata = self.validate_data()
        customer = self.save_customer(vdata)

        # notify listeners (the mailer in this case) that a new customer has registered
        self.notify(events.CustomerRegistered(customer, self.request))

        return {'message': "You have registered successfully"}

    @view_config(context=ValidationFailure, renderer='json')
    def failed_validation(self):
        self.request.response.status_int = 400
        return {'errors': self.request.exception.errors}

    @view_config(context=DatabaseFailure)
    def failed_database(self):
        self.request.response.status_int = 505
        return {'errors': self.request.exception.msg}

    def validate_data(self):
        try:
            return self.schema.deserialize(self.request.params)
        except Invalid as e:
            raise ValidationFailure(e.asdict())

    def save_customer(self, data):
        try:
            customer = Customer(**data)
            self.db.add(customer)
            self.db.flush()
            self.db.refresh(customer)
            return customer
        except exc.IntegrityError as e:
            print(e.args)
            field = e.args[0].split(':')[1].split('.')[1]
            errors = {field: 'This is an already registered value'}
            transaction.abort()
            raise ValidationFailure(errors)
        except exc.SQLAlchemyError as e:
            transaction.abort()
            raise DatabaseFailure(str(e))

