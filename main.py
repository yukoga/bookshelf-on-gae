# *-* coding: utf-8 -*- 

import bookshelf
import config


app = bookshelf.create_app(config)

"""
# @app.route("/")
def hello():
    return "Hello World, hello Flask apps on GAE ! 日本語はどうかな？"
"""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
