#!/usr/bin/env python3

import os
from flask import request
from flask_restful import Resource

from config import create_app, api, db
from models import Book, BookSchema


class Books(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 5
        if per_page > 50:
            per_page = 50

        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": BookSchema(many=True).dump(pagination.items),
        }, 200



api.add_resource(Books, "/books", endpoint="books")

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
