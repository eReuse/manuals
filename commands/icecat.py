import csv
import click
import requests
from pathlib import Path
from datetime import datetime
from time import sleep, mktime

from manager import db
from models import Icecat


class Geticecat:

    def __init__(self, *args, id=None, file=None, **kwargs):
        self.new_ids = []
        self.id = id
        self.file = file
        self.q_icecats = Icecat.query.filter()
        self.get_ids()
        self.get_resources()

    def get_resources(self):
        for id in self.new_ids[:20]:
            base = 'https://live.icecat.biz/api?UserName=openIcecat-live'
            url = f'{base}&Language=en&icecat_id={id}'
            res = requests.get(url).json()
            if not res or res.get('Code') == 404:
                continue
            self.create_icecat(res)
            sleep(5)
        db.session.commit()

    def create_icecat(self, icecat_json):
        info = icecat_json.get('data', {}).get('GeneralInfo', {})
        if not info:
            return

        image = icecat_json.get('Image', {}) or {}
        icecat = Icecat(
            id=info['IcecatId'],
            date=self.get_date(info),
            url=info.get('URL'),
            title=info.get('Title'),
            brand=info.get('Brand'),
            brand_logo=info.get('BrandInfo', {}).get('BrandLogo'),
            product_name=info.get('BrandInfo', {}).get('ProductName'),
            product_serie=info.get('ProductSeries', {}).get('value'),
            family=info.get('ProductFamily', {}).get('value'),
            long_product_name=info.get('Description', {}).get('LongProductName'),
            brand_part_code=info.get('BrandPartCode'),
            image=image.get('HighPic'),
            chassis=info.get("Category", {}).get("Name", {}).get("Value"),
        )
        db.session.add(icecat)

    def get_date(self, info):
        date = info['ReleaseDate']
        if not date:
            return 0
        date_object = datetime.strptime(date, '%d-%m-%Y').date()
        return mktime(date_object.timetuple())

    def get_ids(self):
        f= "icecat_files/icecat_daily_export_urls.txt"
        if self.file:
            f = self.file
        actual_ids = []
        for row in self.q_icecats:
            actual_ids.append(row.id)
        with Path(__file__).parent.joinpath(f).open() as csv_file:
            obj_csv = csv.reader(csv_file, delimiter='\t', quotechar='"')
            _csv = list(obj_csv)
            try:
                for line in _csv[1:]:
                    id = int(line[0])
                    if id in actual_ids:
                        continue
                    self.new_ids.append(id)
            except Exception:
                pass
        self.new_ids = list(set(self.new_ids))


@click.command(name='get_icecat')
def GetIcecat():
    Geticecat()
    print("Finished syncronize Icecat!!")
    return
