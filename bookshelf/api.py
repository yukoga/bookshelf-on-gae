# *-* coding: utf-8 -*- 

from bookshelf import get_model
from flask import Blueprint, render_template, request, abort, jsonify


api = Blueprint("api", __name__)

@api.route("/list")
def list():
    token = request.args.get("page_token", None)
    if token:
        token = token.encode("utf-8")
        
    books, next_page_token = get_model().list(cursor=token)
    
    return jsonify({'books': books})


@api.route("/get/<id>")
def get(id):
    book = get_model().read(id)
    if not book:
        abort(404)
    return jsonify({'book': book})

