# *-* coding: utf-8 -*-

from flask import url_for


def test_app(app):
    assert app


def test_config(client, config):
    assert config['JSON_AS_ASCII'] == False
    assert config['PROJECT_ID'] == 'gcp-jp'
    assert config['DATA_BACKEND'] == 'datastore'
    assert config['SECRET_KEY'] == 'secret'


def test_list(client):
    r = client.get(url_for('api.list'))
    assert r.status_code == 200
    assert 'Google Analytics' in r.data.decode('utf-8')
    assert 'Goggle Analytics' not in r.data.decode('utf-8')


def test_get(client):
    r = client.get(url_for('api.get', id='5668600916475904'))
    assert r.status_code == 200
    assert '追加した本'.decode('utf-8') in r.data.decode('utf-8')
