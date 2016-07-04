# *-* coding: utf-8 -*-

import logging
from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    with app.app_context():
        model = get_model()
        model.init_app(app)

    from .crud import crud
    app.register_blueprint(crud, url_prefix='/books')
    from .api import api
    app.register_blueprint(api, url_prefix='/api/v0.1')

    @app.route('/')
    def index():
        return redirect(url_for('crud.list'))

    @app.route('/list')
    def api_list():
        return redirect(url_for('api.list'))

    @app.route('/get/<id>')
    def api_get(id):
        return redirect(url_for('api.get', id=id))

    @app.errorhandler(404)
    def not_found_error(e):
        return '''
        The URL you accessed is not found in this website.
        Please check the URL in your address bar and try again. <pre>{}</pre>
        '''.format(e), 404

    @app.errorhandler(500)
    def server_error(e):
        return '''
        An internal error occured: <pre>{}</pre>
        See logs for full stacktrace.
        '''.format(e), 500

    return app


def get_model():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'datastore':
        from . import model_datastore
        model = model_datastore
        return model
    else:
        raise ValueError('No appropriate databackend configured.')
