# coding=utf-8

# Database URI, example: mysql://username:password@server/db?charset=utf8mb4
# SQLALCHEMY_DATABASE_URI = ''
pwd="123456"
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+pwd+'@localhost:3306/traffic'
# guniflask configuration
guniflask = dict(
)
