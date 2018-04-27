"""User: Contains all entities that are related to project
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, desc
from evodoc.app import db
import bcrypt

class Project(db.Model):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow())
    update = Column(DateTime, default=datetime.datetime.utcnow())
    active = Column(Boolean)
    data = Column(JSON)

    def __init__(self, name=None, created=None, update=None, active=True, data=None):
        self.name = name
        self.created = created
        self.update = update
        self.active = active
        self.data = data

    def __repr__(self):
        return "<Project %r>" % (self.name)

    @classmethod
    def get_project_by_id(cls, projectId, raiseFlag = True):
        result = cls.query.filter_by(id=projectId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Project not found.")
        return result

    @classmethod
    def get_project_by_name(cls, moduleName, raiseFlag = True):
        result = cls.query.filter_by(name=moduleId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Project not found.")
        return result

    @classmethod
    def get_project_all(cls):
        result = cls.query.all()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Project not found.")
        return result

    @classmethod
    def update_project_name_by_id(cls,projectId,moduleName, raiseFlag = True):
        project = cls.get_project_by_id(projectId, raiseFlag)
        if (project == None):
            return False
        project.name = moduleName
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def update_project_data_by_id(cls,projectId,data, raiseFlag = True):
        project = cls.get_project_by_id(projectId, raiseFlag)
        if (project == None):
            return False
        project.data = data
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def update_project_data_by_name(cls,name,data, raiseFlag = True):
        project = cls.get_project_by_name(name, raiseFlag)
        if (project == None):
            return False
        project.data = data
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def activate_project_by_id(cls, id, raiseFlag = True):
        project = cls.get_project_by_id(id, raiseFlag)
        if (project == None):
            return False
        project.active = True
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def deactivate_project_by_id(cls, id, raiseFlag = True):
        project = cls.get_project_by_id(id, raiseFlag)
        if (project == None):
            return False
        project.active = False
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

