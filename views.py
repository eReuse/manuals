import logging
from flask import Blueprint, jsonify, request
from flask.views import View
from models import Category, Guide, Icecat


logger = logging.getLogger(__name__)


ifixit = Blueprint('ifixit', __name__, url_prefix='/ifixit')


class HomeView(View):
    methods = ['POST']

    def dispatch_request(self):
        try:
            res = self.get_values()
        except Exception as err:
            logger.error("Error: {}".format(err))
            res = {"Ok": "Hello world!"}
        return jsonify(res)

    def get_values(self):
        res = []
        for q in self.query():
            res.append(q.get_json())
        return res

    def query(self):
        req = request.get_json()
        manufacturer = req.get('manufacturer')
        model = req.get('model')
        q = req.get('query')
        if not any([manufacturer, model, q]):
            raise Exception('No there are any query')

        query = Guide.query

        if manufacturer:
            query = query.filter(
                Guide.title.icontains(manufacturer)
            )

        if model:
            query = query.filter(
                Guide.title.icontains(model)
            )

        if q:
            query = query.filter(
                Guide.title.icontains(q)
            )
        return query


ifixit.add_url_rule('/', view_func=HomeView.as_view('home'))
