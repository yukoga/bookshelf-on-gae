# *-* coding: utf-8 -*-

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for, abort


crud = Blueprint('crud', __name__)


@crud.route('/')
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template('list.html', books=books,
                           next_page_token=next_page_token)


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    if not book:
        abort(404)
    return render_template('view.html', book=book)


@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template('form.html', action='Add', book={})


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template('form.html', action='Edit', book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
