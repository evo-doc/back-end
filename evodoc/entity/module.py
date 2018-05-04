"""User: Contains all entities that are related to module
"""
import os
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, Boolean, JSON
from evodoc.entity import db
from evodoc import DbException, ApiException


class Module(db.Model):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    name = Column(String(100), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow())
    update = Column(DateTime, default=datetime.datetime.utcnow())
    active = Column(Boolean)
#    data = Column(JSON)

    def __init__(self, project_id=None, name=None, created=None,
                       update=None, active=True):
        self.project_id = project_id
        self.name = name
        self.created = created
        self.update = update
        self.active = active

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
    def get_module_by_id(cls, moduleId, raiseFlag=True):
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
        res = cls.create_or_update_module_by_id(id, project_id, name, created, update, active, data, raiseFlag)
        return res

    @classmethod
    def create_or_update_module_by_id(cls, id, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        module = None
        if(id is not None):
            module = cls.get_module_by_id(id, False)
        if (module == None):
            res = cls.create_module(project_id, name, created, update, active, data, False)
            return res
        if (module.project_id != project_id and project_id != None):
            if(data == None):
                data = module.data
            res = cls.create_module(project_id, name, created, update, active, data, raiseFlag)
            return res
        changed = 0
        if (name != None):
            m = cls.get_module_by_name(name,False)
            if (m != None):
                if (m.id != id) and raiseFlag:
                    raise DbException(400, "Name is already taken")
                    return None
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
            #save "data"
            with open(os.path.dirname(__file__) + '/../../data/module/' + 
                      str(module.project_id) + '/' + str(module.id) + '.md', 'w') as f:
                f.write(data)
        if (update != None):
            changed = 0
            module.update = update
            db.session.commit()
            return module
        if (changed == 1):
            module.update = datetime.datetime.utcnow()
            db.session.commit()
            return module
        return None

    @classmethod
    def create_module(cls, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        if (None != cls.get_module_by_name(name,False)):
            if raiseFlag:
                raise DbException(400, "Name is already taken")
            return None
        entity = Module(project_id=project_id, name=name, created=created, update=update, active=active)
        entity.save_entity()
        #save "data"
        with open(os.path.dirname(__file__) + '/../../data/module/' + 
                  str(entity.project_id) + '/' + str(entity.id) + '.md', 'w') as f:
            f.write(data)
        return entity
