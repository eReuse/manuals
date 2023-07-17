import datetime

from sqlalchemy import BigInteger, SmallInteger, Column, ForeignKey, UnicodeText
from sqlalchemy.orm import backref, relationship
from manager import db


class Category(db.Model):
    id = Column(BigInteger, primary_key=True)
    name = Column(UnicodeText(), nullable=True)


class Guide(db.Model):
    id = Column(BigInteger, primary_key=True)
    date = Column(BigInteger, nullable=False)
    url = Column(UnicodeText(), nullable=True)
    title = Column(UnicodeText(), nullable=True)
    image_guid = Column(UnicodeText(), nullable=True)
    category_id = Column(BigInteger, ForeignKey(Category.id), nullable=False)
    category = relationship(
        Category,
        backref=backref('guides', lazy=True, cascade="all,delete"),
        primaryjoin=Category.id == category_id,
    )

    @property
    def image(self):
        img = self.image_guid
        if not img:
            return ''
        url = f'https://guide-images.cdn.ifixit.com/igi/{img}.full'
        return url

    def get_json(self):
        return {
            'url': self.url,
            'image': self.image,
            'title': self.title,
            'category': self.category.name
        }


class Icecat(db.Model):
    id = Column(BigInteger, primary_key=True)
    date = Column(BigInteger, nullable=False)
    url = Column(UnicodeText(), nullable=True)
    title = Column(UnicodeText(), nullable=True)
    image = Column(UnicodeText(), nullable=True)
    brand = Column(UnicodeText(), nullable=True)
    brand_logo = Column(UnicodeText(), nullable=True)
    product_name = Column(UnicodeText(), nullable=True)
    product_serie = Column(UnicodeText(), nullable=True)
    long_product_name = Column(UnicodeText(), nullable=True)
    brand_part_code = Column(UnicodeText(), nullable=True)
    chassis = Column(UnicodeText(), nullable=True)
    family = Column(UnicodeText(), nullable=True)

    @property
    def pdf(self):
        id = self.id
        if not id:
            return ''
        url = f'https://icecat.biz/rest/product-pdf?productId={id}&lang=en'
        return url

    @property
    def datetime(self):
        return datetime.datetime.fromtimestamp(self.date)

    @property
    def date_str(self):
        return datetime.datetime.fromtimestamp(self.date).strftime("%d/%m/%Y")

    def get_json(self):
        return {
            'url': self.url,
            'logo': self.brand_logo,
            'title': self.title,
            'pdf': self.pdf,
            "image": self.image,
        }


class Laer(db.Model):
    id = Column(BigInteger, primary_key=True)
    code = Column(UnicodeText(), nullable=True)
    metal = Column(SmallInteger(), nullable=True)
    plastic_post_consumer = Column(SmallInteger(), nullable=True)
    plastic_post_industry = Column(SmallInteger(), nullable=True)


class computer_laer(db.Model):
    id = Column(BigInteger, primary_key=True)
    title = Column(UnicodeText(), nullable=False)
    laer_id = Column(BigInteger, ForeignKey(Laer.id), nullable=False)
    laer = relationship(
        Laer,
        backref=backref('computers', lazy=True, cascade="all,delete"),
        primaryjoin=Laer.id == laer_id,
    )

    def get_json(self):
        return {
            'code': self.laer.code,
            'metal': self.laer.metal,
            'plastic_post_consumer': self.laer.plastic_post_consumer,
            'plastic_post_industry': self.laer.plastic_post_industry
        }
