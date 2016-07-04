# *-* coding: utf-8 -*-

import config
from tests.conftest import *


def test_app(app):
    assert app


def test_config(client):
    assert config.JSON_AS_ASCII == False
    assert config.PROJECT_ID == 'gcp-jp'
    assert config.DATA_BACKEND == 'datastore'
    assert config.SECRET_KEY == 'secret'
