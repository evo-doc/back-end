import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from flask import current_app
from evodoc.entity import db
from evodoc import DbException
from git import Git

git_path = ''

class Package(db.Model):
    __tablename__ = "package"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    url = Column(String(255))
    created = Column(DateTime, default=datetime.datetime.utcnow())
    update = Column(DateTime, default=datetime.datetime.utcnow())
    active = Column(Boolean, default=True)

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return "<Package %r on %r>" % (self.name, self.url)

    @classmethod
    def get_package_by_id(cls, packageId, raiseFlag=True):
        package = Package.query.filter_by(id=packageId).first()
        if (package is None) and raiseFlag:
            raise DbException(404, "Package with id: %r not found"%(packageId))
        return package

    @classmethod
    def get_all_packages(cls):
        packages = Package.query.all()
        return packages

    @classmethod
    def delete_package(cls):
        cls.active = False
        cls.update = datetime.datetime.utcnow()
        db.session.commit()

    @classmethod
    def save_or_create(cls, data):
        package = None
        if 'package_id' in data or not data['package_id']:
            package = Package()
        else:
            package = cls.get_package_by_id(data['package_id'], False)
            if package is None:
                package = Package()
                data['package_id'] = ''
        if 'url' in data and not data['url']:
            package.url = data['url']
            package.update = datetime.datetime.utcnow()
        if 'name' in data and not data['name']:
            package.name = data['name']
            package.update = datetime.datetime.utcnow()

        if not package.id:
            db.session.add(package)
        db.session.commit()
        return package

    @classmethod
    def clone_repository(cls):
        Git(git_path).clone(cls.url + '.git')
        return True

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'created': self.created,
            'update': self.update,
            'active': self.active,
        }

