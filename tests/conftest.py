import sys
import os

from evodoc import create_app
from evodoc.entity import db as _db
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from pytest import fixture
from flask_migrate import upgrade, Migrate

@fixture(scope="class")
def app(request):
    """
    Returns session-wide application.
    """
    test_settings = {
        'TEST': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,
        'SQLALCHEMY_DATABASE_URI': "sqlite:////tmp/evodoc.db"
    }

    _app = create_app(test_settings)

    _app.app_context().push()

    yield _app

@fixture(scope="class")
def db(app, request):
    """
    Returns session-wide initialised database.
    """
    #perform upgrade
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield _db


@fixture(scope="class", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        _db.session = sess
        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
