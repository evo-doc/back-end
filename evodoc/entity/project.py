"""User: Contains all entities that are related to project
"""
import os
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, desc
from evodoc.entity import db
from evodoc import DbException, ApiException
import bcrypt

class Project(db.Model):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow())
    update = Column(DateTime, default=datetime.datetime.utcnow())
    active = Column(Boolean)

    def __init__(self, name=None, created=None, update=None, active=True):
        self.name = name
        self.created = created
        self.update = update
        self.active = active

    def __repr__(self):
        return "<Project %r>" % (self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'update': self.update,
            'active': self.active,
        }

    @classmethod
    def get_project_by_id(cls, projectId, raiseFlag = True):
        result = cls.query.filter_by(id=projectId).first()
        if (result == None) & raiseFlag:
            raise DbException(404, "Project not found.")
        return result

    @classmethod
    def get_project_by_name(cls, projectName, raiseFlag = True):
        result = cls.query.filter_by(name=projectName).first()
        if (result == None) & raiseFlag:
            raise DbException(404, "Project not found.")
        return result

    @classmethod
    def get_project_all(cls, raiseFlag = True):
        result = cls.query.all()
        if (result == None) & raiseFlag:
            raise DbException(404, "Project not found.")
        return result

    @classmethod
    def update_project_name_by_id(cls,projectId,projectName, raiseFlag = True):
        project = cls.get_project_by_id(projectId, raiseFlag)
        if (project == None):
            return False
        project.name = projectName
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

#    @classmethod
#    def update_project_data_by_id(cls,projectId,data, raiseFlag = True):
#        project = cls.get_project_by_id(projectId, raiseFlag)
#        if (project == None):
#            return False
#        project.data = data
#        project.update = datetime.datetime.utcnow()
#        db.session.commit()
#        return True

#    @classmethod
#    def update_project_data_by_name(cls,name,data, raiseFlag = True):
#        project = cls.get_project_by_name(name, raiseFlag)
#        if (project == None):
#            return False
#        project.data = data
#        project.update = datetime.datetime.utcnow()
#        db.session.commit()
#        return True

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

    @classmethod
    def create_project(cls, name=None, created=None, update=None, active=True, raiseFlag = True):
        p = None
        if (cls.get_project_by_name(name,False) != None):
            if(raiseFlag):
                DbException(400, "Name is already taken")
            return p
        p = Project(name, created, update, active)
        db.session.add(p)
        db.session.commit()
        os.mkdir(os.path.dirname(__file__) + '/../../data/module/' + str(p.id))
        return p

    @classmethod
    def update_project_by_id(cls, id, name=None, created=None, update=None,
                                 active=True, raiseFlag = True):
        p = cls.get_project_by_id(id,raiseFlag)
        changed = 0
        if (name != None):
            p.name = name
            changed = 1
        if (created != None):
            p.created = created
            changed = 1
        if (active != None):
            p.active = active
            changed = 1
        if (update != None):
            p.update = update
            db.session.commit()
        else:
            if (changed == 1):
                p.update = datetime.datetime.utcnow()
                db.session.commit()
        return p

    @classmethod
    def create_or_update_project_by_id(cls, id, name=None, created=None, update=None,
                                       active=True, raiseFlag = True):
        p = None
        if (id is not None):
            p = cls.get_project_by_id(id,False)
        if (p == None):
            p = cls.create_project(name, created, update, active, raiseFlag)
            return p
        p = cls.update_project_by_id(id, name, created, update, active, raiseFlag)
        return p

    @classmethod
    def create_or_update_project_by_id_array(cls, id, array, raiseFlag = True):
        #######################################################################
        if (('name' not in array) or (array['name'] == None)):
            name = None
        else:
            name = array['name']
        #######################################################################
        if (('created' not in array) or (array['created'] == None)):
            created = None
        else:
            created = array['created']
        #######################################################################
        if (('update' not in array) or (array['update'] == None)):
            update = None
        else:
            update = array['update']
        #######################################################################
        if (('active' not in array) or (array['active'] == None)):
            active = None
        else:
            active = array['active']
        #######################################################################
        p = cls.create_or_update_project_by_id(id, name, created, update, active, raiseFlag)
        return p
