import logging
from flask import Blueprint, jsonify
from flask.views import View
from models import Category, Guide, Icecat


logger = logging.getLogger(__name__)


ifixit = Blueprint('ifixit', __name__, url_prefix='/ifixit')


class HomeView(View):
    def dispatch_request(self, name="World"):
        res = {"Ok": f"Hello {name}!"}
        return jsonify(res)


ifixit.add_url_rule('/<string:name>', view_func=HomeView.as_view('home'))
