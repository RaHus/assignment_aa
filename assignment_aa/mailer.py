from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from pyramid.events import subscriber
from .events import CustomerRegistered


@subscriber(CustomerRegistered)
def notify_admin_user_registered(event):
    """ Send an email to 'reports.recipient' whenever a user registers
        using a different template for any contract and customer type
        combination
    """
    mailer = get_mailer(event.request)

    jenv = event.request.jinja2_env
    template_name = 'templates/reports/%s-%s.jinja2' % (event.customer.contract_type.lower().replace(' ', ''),
                                                        event.customer.customer_type.lower().replace(' ', ''))
    template = jenv.get_template(template_name)

    message = Message(subject="A new user has registered",
                      sender="registration@assignment_aa.local",
                      recipients=[event.request.registry.settings['reports.recipient']],
                      body=template.render(customer=event.customer))

    #mailer.send_to_queue(message)
    mailer.send(message)

