import logging
from flask import Blueprint, jsonify, request
from flask.views import View
from models import Category, Guide, Icecat


logger = logging.getLogger(__name__)


ifixit = Blueprint('ifixit', __name__, url_prefix='/')


class ManualsMix(View):
    methods = ['POST']

    def dispatch_request(self):
        try:
            self.get_params()
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

    def get_params(self):
        req = request.get_json()
        self.manufacturer = req.get('manufacturer')
        self.model = req.get('model')
        self.q = req.get('query')
        if not any([self.manufacturer, self.model, self.q]):
            raise Exception('No there are any query')

    def query(self):
        """
            Need to implement
        """
        return []


class IfixitView(ManualsMix):
    def query(self):
        query = Guide.query

        if self.manufacturer:
            query = query.filter(
                Guide.title.icontains(self.manufacturer)
            )

        if self.model:
            query = query.filter(
                Guide.title.icontains(self.model)
            )

        if self.q:
            query = query.filter(
                Guide.title.icontains(self.q)
            )
        return query


class IcecatView(ManualsMix):
    def query(self):
        query = Guide.query

        if self.manufacturer:
            query = query.filter(
                Guide.title.icontains(self.manufacturer)
            )

        if self.model:
            query = query.filter(
                Guide.title.icontains(self.model)
            )

        if self.q:
            query = query.filter(
                Guide.title.icontains(self.q)
            )
        return query


ifixit.add_url_rule('/ifixit', view_func=IfixitView.as_view('ifixit'))
ifixit.add_url_rule('/icecat', view_func=IcecatView.as_view('icecat'))
