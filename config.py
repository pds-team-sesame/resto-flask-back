class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/pds'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'rootroot'