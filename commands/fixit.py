import click
import requests
from time import sleep

from manager import db
from models import Category, Guide


class Fixit:

    def __init__(self, *args, limit=200, offset=0, **kwargs):
        self.new_guides_json = []
        self.start = True
        self.limit = limit
        self.offset = offset
        self.plus = 200
        self.q_guides = Guide.query.filter()
        self.q_category = Category.query.filter()
        self.reset_offset()
        self.get_resources()

    def reset_offset(self):
        last_guide = self.q_guides.order_by(Guide.id.desc()).first()
        if last_guide:
            self.offset = last_guide.id + 1

    def get_resources(self):
        while self.start:
            base = 'https://www.ifixit.com/api/2.0/guides?'
            limit = self.limit
            offset = self.offset
            url = f'{base}limit={limit}&offset={offset}'
            res = requests.get(url).json()
            if not res:
                self.start = False
                return
            self.new_guides_json.extend(res)
            self.offset += self.plus
            self.create_guides()
            sleep(5)

    def create_guides(self):
        for guide in self.new_guides_json:
            self.create_guide(guide)
        self.new_guides_json = []
        db.session.commit()

    def create_guide(self, guide_json):
        category_name = guide_json.get('category')
        image = guide_json.get('image', {}) or {}
        guide = Guide(
            id=guide_json['guideid'],
            date=guide_json['modified_date'],
            url=guide_json['url'],
            title=guide_json['title'],
            image_guid=image.get('guid'),
            category=self.get_category(category_name)
        )
        db.session.add(guide)

    def get_category(self, name):
        category = self.q_category.filter(Category.name==name).first()
        if category:
            return category
        category = Category(name=name)
        db.session.add(category)
        return category


@click.command(name='get_fixit')
def GetFixit():
    Fixit()
    print("Finished syncronize Fixit!!")
    return
