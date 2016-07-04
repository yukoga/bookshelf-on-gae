# *-* coding: utf-8 -*-

import bookshelf
import config
import pytest


@pytest.fixture
def app():
    app = bookshelf.create_app(config)
    return app
