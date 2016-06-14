from pyramid.config import Configurator
import pyramid_jinja2


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()

    config.commit()

    config.add_request_method(
        lambda x: config.get_jinja2_environment(),
        'jinja2_env',
        reify=True
    )

    return config.make_wsgi_app()
