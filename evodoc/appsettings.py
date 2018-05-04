class AppSettings:
    DEBUG = False
    DEVELOPMENT = False
    TEST = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
    GIT_PATH = "../packages_git"