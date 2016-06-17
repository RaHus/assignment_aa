import unittest
from unittest.mock import MagicMock
from sqlalchemy import exc

import transaction

from pyramid import testing

from assignment_aa.models import Customer


def dummy_request(dbsession, **kw):
    return testing.DummyRequest(dbsession=dbsession, **kw)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///assignment_aa_test.sqlite',
            'pyramid.includes': ['pyramid_mailer.debug'],
            'reports.recipient': 'testrecipient@test.local'

        })
        self.config.include('.models')
        settings = self.config.get_settings()
        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def test_passing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info['project'], 'assignment_aa')


class TestCustomerFormSuccessCondition(BaseTest):

    def setUp(self):
        from .models import Customer

        super(TestCustomerFormSuccessCondition, self).setUp()
        self.init_database()

        self.model = Customer(name='test', email='test@email.com')
        self.session.add(self.model)

    def test_passing_view(self):
        from .views.customer import CustomerFormView
        classview = CustomerFormView(dummy_request(self.session))
        info = classview.customer_form()
        self.assertTrue(info.get('const', False))

    def test_failing_view(self):
        from .views.customer import CustomerFormView, DatabaseFailure
        req = testing.DummyRequest(dbsession=self.session, exception=DatabaseFailure('test'))
        classview = CustomerFormView(req)
        info = classview.failed_database()
        self.assertTrue('errors' in info)

    def test_failing_db_view(self):
        from .views.customer import CustomerFormView, DatabaseFailure
        params = {'name': 'test',
                  'email': 'test@test.local',
                  'customer_type': 'Direct',
                  'contract_type': 'One Time'}
        req = testing.DummyRequest(dbsession=self.session, params=params)
        classview = CustomerFormView(req)

        with unittest.mock.patch.object(classview.db, 'flush') as flushMock:
            flushMock.side_effect = exc.DatabaseError('', '', '')
            with self.assertRaises(exc.SQLAlchemyError):
                classview.customer_form_save()

    def test_model_repr(self):
        self.assertTrue("<Customer" in self.model.__repr__())


class CustomerFunctionalTests(BaseTest):
    def setUp(self):
        from .models import Customer

        super(CustomerFunctionalTests, self).setUp()
        self.init_database()

        from assignment_aa import main
        app = main({}, **self.config.registry.settings)
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'<p class="lead">Welcome to <span class="font-normal">assignment_aa</span>' in res.body)

    def test_fails_404_view(self):
        res = self.testapp.get('/invalid', status=404)
        self.assertTrue(b'404</span> Page Not Found' in res.body)

    def test_form_view(self):
        res = self.testapp.get('/form', status=200)
        self.assertTrue(b'<form method="POST" action="form">' in res.body)

    def test_fails_validation_form_post(self):
        data = {b'name': 'test0'*10,
                b'email': 'test@test.local'*10,
                b'customer_type': 'invalid',
                b'contract_type': 'invalid'}
        res = self.testapp.post('/form', data, status=400)

        self.assertIn(b'errors', res.body)
        for key in data:
            self.assertIn(key, res.body)

    def test_successfull_form_post(self):
        data = {b'name': 'test',
                b'email': 'test@test.local',
                b'customer_type': 'Direct',
                b'contract_type': 'One Time'}
        res = self.testapp.post('/form', data, status=200)
        self.assertIn(b'message', res.body)

    def test_fails_form_post(self):
        data = {b'name': 'test',
                b'email': 'test@test.local',
                b'customer_type': 'Direct',
                b'contract_type': 'One Time'}
        self.testapp.post('/form', data, status=200)
        res = self.testapp.post('/form', data, status=400)
        self.assertIn(b'errors', res.body)
