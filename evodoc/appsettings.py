class AppSettings:
    """
    Global settings for evodoc
    """
    DEBUG = False
    DEVELOPMENT = False
    TEST = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/evodoc.db"
    GIT_PATH = "../packages_git"