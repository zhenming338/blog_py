class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:river@127.0.0.1:3307/article"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret-key"
    JWT_SELECT_KEY = "this_is_jwt_secret_key_by_river"
