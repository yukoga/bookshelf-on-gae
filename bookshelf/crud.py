# *-* coding: utf-8 -*- 

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint("crud", __name__)

@crud.route("/")
def list():
    token = request.args.get("page_token", None)
    if token:
        token = token.encode("utf-8")
        
    books, next_page_token = get_model().list(cursor=token)
    
    return render_template("list.html",
                           books=books,
                           next_page_token=next_page_token)

@crud.route("/<id>")
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)

