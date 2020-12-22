# coding=utf-8

from testtrail import db


class Trail(db.Model):
    __tablename__ = 'trail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    date_time = db.Column(db.DateTime, comment='时间')
    latitude = db.Column(db.String(255), comment='经度')
    longitude = db.Column(db.String(255), comment='纬度')
    imei = db.Column(db.String(255), comment='imei唯一标识')
    type = db.Column(db.String(255), comment='哪一段路程（北辰东路，两广路）')
