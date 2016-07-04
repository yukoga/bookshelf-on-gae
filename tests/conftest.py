# *-* coding: utf-8 -*-

from flask import url_for
import bookshelf
import config
import pytest


@pytest.fixture(scope="session")
def app():
    app = bookshelf.create_app(config)
    return app
