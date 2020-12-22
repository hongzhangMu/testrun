# coding=utf-8

from testtrail import db


class TestRoadsName(db.Model):
    __tablename__ = 'test_roads_name'

    id = db.Column(db.Integer, primary_key=True, comment='ID')
    type = db.Column(db.String(255), comment='类型')
    name = db.Column(db.String(255), comment='名称')
