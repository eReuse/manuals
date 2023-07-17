import json
import logging
from flask import Blueprint, jsonify, request
from flask.views import View
from sqlalchemy import or_
from models import Guide, Icecat, computer_laer
from models import Category


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
            res = []
        return jsonify(res)

    def get_values(self):
        res = []
        for q in self.query():
            res.append(q.get_json())
        return res

    def get_params(self):
        req = json.loads(request.data)
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


class LaerView(ManualsMix):
    def query(self):
        query = computer_laer.query

        if self.manufacturer:
            query = query.filter(
                computer_laer.title.icontains(self.manufacturer)
            )

        if self.model:
            query = query.filter(
                computer_laer.title.icontains(self.model)
            )

        if self.q:
            query = query.filter(
                computer_laer.title.icontains(self.q)
            )
        return query


class IcecatView(ManualsMix):
    def query(self):
        query = Icecat.query

        if self.manufacturer:
            query = query.filter(
                or_(
                    Icecat.title.icontains(self.manufacturer),
                    Icecat.brand.icontains(self.manufacturer),
                    Icecat.product_name.icontains(self.manufacturer),
                    Icecat.long_product_name.icontains(self.manufacturer),
                )
            )

        if self.model:
            query = query.filter(
                or_(
                    Icecat.title.icontains(self.model),
                    Icecat.brand.icontains(self.model),
                    Icecat.product_name.icontains(self.model),
                    Icecat.long_product_name.icontains(self.model),
                )
            )

        if self.q:
            query = query.filter(
                or_(
                    Icecat.title.icontains(self.q),
                    Icecat.brand.icontains(self.q),
                    Icecat.product_name.icontains(self.q),
                    Icecat.long_product_name.icontains(self.q),
                )
            )
        return query


ifixit.add_url_rule('/ifixit', view_func=IfixitView.as_view('ifixit'))
ifixit.add_url_rule('/icecat', view_func=IcecatView.as_view('icecat'))
ifixit.add_url_rule('/laer', view_func=LaerView.as_view('laer'))
