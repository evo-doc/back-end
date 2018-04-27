"""User: Contains all entities that are related to module and project
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, desc
from evodoc.app import db
import bcrypt

class Module(db.Model):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    name = Column(String(50), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow())
    update = Column(DateTime, default=datetime.datetime.utcnow())
    active = Column(Boolean)
    data = Column(JSON)

    def __init__(self, project_id=None, name=None, created=None, update=None, active=True, data=None):
        self.project_id = project_id
        self.name = name
        self.created = created
        self.update = update
        self.active = active
        self.data = data

    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'created': self.created,
            'update': self.update,
            'active': self.active,
            'data': self.data,
        }

    def __repr__(self):
        return "<Module %r>" % (self.name)

    @classmethod
    def get_module_by_id(cls, moduleId, raiseFlag = True):
        result = cls.query.filter_by(id=moduleId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Module not found.")
        return result

    @classmethod
    def get_module_by_name(cls, moduleName, raiseFlag = True):
        result = cls.query.filter_by(name=moduleName).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Module not found.")
        return result

    @classmethod
    def get_module_all(cls, raiseFlag = True):
        result = cls.query.all()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Module not found.")
        return result

    @classmethod
    def get_module_all_by_project_id(cls, projectId, raiseFlag = True):
        result = cls.query.filter_by(project_id=projectId).all()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "Module not found.")
        return result

    @classmethod
    def update_name_by_id(cls,moduleId,moduleName, raiseFlag = True):
        module = cls.get_module_by_id(moduleId, raiseFlag)
        if (module == None):
            return False
        if (None != self.get_module_by_name(moduleName,false)):
            if raiseFlag:
                raise DbException(400, "Name is already taken")
            return false
        module.name = moduleName
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def update_module_data_by_id(cls,moduleId,data, raiseFlag = True):
        module = cls.get_module_by_id(moduleId, raiseFlag)
        if (module == None):
            return False
        module.data = data
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def update_module_data_by_name(cls,name,data, raiseFlag = True):
        module = cls.get_module_by_name(name, raiseFlag)
        if (module == None):
            return False
        module.data = data
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def activate_module_by_id(cls, id, raiseFlag = True):
        module = cls.get_module_by_id(id, raiseFlag)
        if (module == None):
            return False
        module.active = True
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def deactivate_module_by_id(cls, id, raiseFlag = True):
        module = cls.get_module_by_id(id, raiseFlag)
        if (module == None):
            return False
        module.active = False
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def save_entity(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_or_update_module_by_id_from_array(cls,id,array, raiseFlag = True):
        if (('project_id' not in array) or (array['project_id'] == None)):
            project_id = None
        else:
            project_id = array['project_id']
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
        if (('data' not in array) or (array['data'] == None)):
            data = None
        else:
            data = array['data']
        #######################################################################
        if (cls.create_or_update_module_by_id(id, project_id, name, created, update, active, data, raiseFlag) == False): 
            return False
        return True

    @classmethod
    def create_or_update_module_by_id(cls, id, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        module = None
        if(id is not None):
            module = cls.get_module_by_id(id, False)
        if (module == None):
            if (cls.create_module(project_id, name, created, update, active, data, raiseFlag) == False):
                return False
            return True
        if (module.project_id != project_id and project_id != None):
            if(data == None):
                data = module.data
            if (cls.create_module(project_id, name, created, update, active, data, raiseFlag) == False):
                return False
            return True
        changed = 0
        if (name != None):
            if (cls.get_module_by_name(name,False) != None):
                if raiseFlag:
                    raise DbException(400, "Name is already taken")
                return False
            changed = 1
            module.name = name
        if (created != None):
            changed = 1
            module.created = created
        if (active != None):
            changed = 1
            module.active = active
        if (data != None):
            changed = 1
            module.data = data
        if (update != None):
            changed = 0
            module.update = update
            db.session.commit()
            return True
        if (changed == 1):
            module.update = datetime.datetime.utcnow()
            db.session.commit()
        return True

    @classmethod
    def create_module(cls, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        if (None != cls.get_module_by_name(name,False)):
            if raiseFlag:
                raise DbException(400, "Name is already taken")
            return False
        entity = Module(project_id=project_id, name=name, created=created, update=update, active=active, data=data)
        entity.save_entity()
        return True

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

