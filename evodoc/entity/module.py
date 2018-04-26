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

    def __repr__(self):
        return "<Module %r>" % (self.name)

    def get_module_by_id(self, moduleId, raiseFlag = True):
        result = self.query.filter_by(id=moduleId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def get_module_by_name(self, moduleName, raiseFlag = True):
        result = self.query.filter_by(name=moduleId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def get_module_all(self, raiseFlag = True):
        result = self.query.all()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def get_module_all_by_project_id(self, projectId, raiseFlag = True):
        result = self.query.filter_by(project_id=projectId).all()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def update_name_by_id(self,moduleId,moduleName, raiseFlag = True):
        module = self.get_module_by_id(moduleId, raiseFlag)
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

    def update_module_data_by_id(self,moduleId,data, raiseFlag = True):
        module = self.get_module_by_id(moduleId, raiseFlag)
        if (module == None):
            return False
        module.data = data
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def update_module_data_by_name(self,name,data, raiseFlag = True):
        module = self.get_module_by_name(name, raiseFlag)
        if (module == None):
            return False
        module.data = data
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def activate_module_by_id(self, id, raiseFlag = True):
        module = self.get_module_by_id(id, raiseFlag)
        if (module == None):
            return False
        module.active = True
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def deactivate_module_by_id(self, id, raiseFlag = True):
        module = self.get_module_by_id(id, raiseFlag)
        if (module == None):
            return False
        module.active = False
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def save_entity(self):
        db.session.add(self)
        db.session.commit()

    def create_or_update_module_by_id_from_array(self,id,array, raiseFlag = True):
        if (self.create_or_update_module_by_id(id, array['project_id'], array['name'], array['created'], array['update'], array['active'], array['data'], raiseFlag) == False): 
            return False
        return True

    def create_or_update_module_by_id(self, id, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        print(self)
        module = self.get_module_by_id(id)
        if (module == None):
            if (self.create_module(project_id, name, created, update, active, data, raiseFlag) == False):
                return False
            return True
        if (module.project_id != project_id and project_id != None):
            if(data == None):
                data = module.data
            if (self.create_module(project_id, name, created, update, active, data, raiseFlag) == False):
                return False
            return True
        changed = 0
        if (name != None):
            if (self.get_module_by_name(name,False) != None):
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
            module.data = dataArray
        if (update != None):
            changed = 0
            module.update = update
            db.session.commit()
            return True
        if (changed == 1):
            module.update = datetime.datetime.utcnow()
            db.session.commit()
        return True

    def create_module(self, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        if (None != self.get_module_by_name(name,False)):
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

    def get_project_by_id(self, projectId, raiseFlag = True):
        result = self.query.filter_by(id=projectId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def get_project_by_name(self, moduleName, raiseFlag = True):
        result = self.query.filter_by(name=moduleId).first()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def get_project_all(self):
        result = self.query.all()
        if (result == None) & raiseFlag:
            raise DbException(DbException, 404, "User not found.")
        return result

    def update_project_name_by_id(self,projectId,moduleName, raiseFlag = True):
        project = self.get_project_by_id(projectId, raiseFlag)
        if (project == None):
            return False
        project.name = moduleName
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def update_project_data_by_id(self,projectId,data, raiseFlag = True):
        project = self.get_project_by_id(projectId, raiseFlag)
        if (project == None):
            return False
        project.data = data
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def update_project_data_by_name(self,name,data, raiseFlag = True):
        project = self.get_project_by_name(name, raiseFlag)
        if (project == None):
            return False
        project.data = data
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def activate_project_by_id(self, id, raiseFlag = True):
        project = self.get_project_by_id(id, raiseFlag)
        if (project == None):
            return False
        project.active = True
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def deactivate_project_by_id(self, id, raiseFlag = True):
        project = self.get_project_by_id(id, raiseFlag)
        if (project == None):
            return False
        project.active = False
        project.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

