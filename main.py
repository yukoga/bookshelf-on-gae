# *-* coding: utf-8 -*-

import bookshelf
import config


app = bookshelf.create_app(config)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
