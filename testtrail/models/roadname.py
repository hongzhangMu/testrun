# coding=utf-8

from testtrail import db


class Roadname(db.Model):
    __tablename__ = 'roadname'

    id = db.Column(db.Integer, primary_key=True, comment='id')
    name = db.Column(db.String(255), comment='路口名字')
    latitude = db.Column(db.String(255), comment='经度')
    longitude = db.Column(db.String(255), comment='纬度')
    roadsection = db.Column(db.String(255), comment='路段')
    distance = db.Column(db.Float, comment='距离')
    greenstart_time = db.Column(db.TIME, comment='绿灯启亮时刻')
    ns_green_time = db.Column(db.String(255), comment='南北绿灯时间')
    ns_yellow_time = db.Column(db.String(255), comment='南北黄灯时间')
    ns_red_time = db.Column(db.String(255), comment='南北红灯时间')
    type = db.Column(db.String(255), comment='ÀàÐÍ12345')
