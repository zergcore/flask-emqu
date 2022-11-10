class Config():
    SECRET_KEY='SUPER SECRET'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=True