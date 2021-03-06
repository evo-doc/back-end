"""User: Contains all entities that are related to module
"""
import os
import datetime
from evodoc.entity.project import Project
from evodoc.entity import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, Boolean, JSON
from evodoc import DbException, ApiException


class Module(db.Model):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    name = Column(String(100), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow())
    update = Column(DateTime, default=datetime.datetime.utcnow())
    active = Column(Boolean)

    def __init__(self, project_id=None, name=None, created=None,
                       update=None, active=True):
        self.project_id = project_id
        self.name = name
        self.created = created
        self.update = update
        self.active = active

    def serialize(self):
        """
        Serialize object for json
            :param self:
        """
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'created': self.created,
            'update': self.update,
            'active': self.active,
            'data': self.get_data(),
        }

    def __repr__(self):
        return "<Module %r>" % (self.name)

    @classmethod
    def get_module_by_id(cls, moduleId, raiseFlag=True):
        """
            Returns module found by ID.
            :param cls: Module
            :param moduleId:
            :param raiseFlag: If True and Module not found raises DbException
        """
        result = cls.query.filter_by(id=moduleId).first()
        if (result == None) & raiseFlag:
            raise DbException(404, "Module not found.")
        return result

    @classmethod
    def get_module_by_name(cls, moduleName, raiseFlag = True):
        """
            Returns module found by name.
            :param cls: Module
            :param moduleName:
            :param raiseFlag: If True and Module not found raises DbException
        """
        result = cls.query.filter_by(name=moduleName).first()
        if (result == None) & raiseFlag:
            raise DbException(404, "Module not found.")
        return result

    @classmethod
    def get_module_all(cls, raiseFlag = True):
        """
            Returns all modules.
            :param cls: Module
            :param raiseFlag: If True and Module not found raises DbException
        """
        result = cls.query.all()
        if (result == None or result == []) & raiseFlag:
            raise DbException(404, "Module not found.")
        return result

    @classmethod
    def get_module_all_by_project_id(cls, projectId, raiseFlag = True):
        """
            Returns all modules in one project.
            :param cls: Module
            :param projectId:
            :param raiseFlag: If True and Module not found raises DbException
        """
        result = cls.query.filter_by(project_id=projectId).all()
        if (result == None or result == []) & raiseFlag:
            raise DbException(404, "Module not found.")
        return result

#    @classmethod
#    def update_name_by_id(cls,moduleId,moduleName, raiseFlag = True):
#        module = cls.get_module_by_id(moduleId, raiseFlag)
#        if (module == None):
#            return False
#        if (None != self.get_module_by_name(moduleName,false)):
#            if raiseFlag:
#                raise DbException(400, "Name is already taken")
#            return false
#        module.name = moduleName
#        module.update = datetime.datetime.utcnow()
#        db.session.commit()
#        return True

#    @classmethod
#    def update_module_data_by_id(cls,moduleId,data, raiseFlag = True):
#        module = cls.get_module_by_id(moduleId, raiseFlag)
#        if (module == None):
#            return False
#        module.data = data
#        module.update = datetime.datetime.utcnow()
#        db.session.commit()
#        return True

#    @classmethod
#    def update_module_data_by_name(cls,name,data, raiseFlag = True):
#        module = cls.get_module_by_name(name, raiseFlag)
#        if (module == None):
#            return False
#        module.data = data
#        module.update = datetime.datetime.utcnow()
#        db.session.commit()
#        return True

    @classmethod
    def activate_module_by_id(cls, id, raiseFlag = True):
        """
            Activate module found by ID.
            :param cls: Module
            :param moduleId:
            :param raiseFlag: If True and Module not found raises DbException
        """
        module = cls.get_module_by_id(id, raiseFlag)
        if (module == None):
            return False
        module.active = True
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def deactivate_module_by_id(cls, id, raiseFlag = True):
        """
            Deactivates module found by ID.
            :param cls: Module
            :param moduleId:
            :param raiseFlag: If True and Module not found raises DbException
        """
        module = cls.get_module_by_id(id, raiseFlag)
        if (module == None):
            return False
        module.active = False
        module.update = datetime.datetime.utcnow()
        db.session.commit()
        return True

    def save_entity(self):
        """
            Saves entity. Function is unguarded and its expected that all data being inserted are correct.
            :param self: Instance of Module class
        """ 
        db.session.add(self)
        db.session.commit()

    def get_data(self, raiseFlag = True):
        """
            Returns data from module.
            :param self: Instance of Module class
            :param raiseFlag: If True and Module not found raises DbException
        """
        try:
            with open(os.path.dirname(__file__) + '/../../data/module/' + 
                      str(self.project_id) + '/' + str(self.id) + '.md', 'r') as f:
                data = f.read()
            return data
        except FileNotFoundError:
            if raiseFlag:
                raise DbException(404, "Module data not found.")
            return None

    @classmethod
    def create_or_update_module_by_id_from_array(cls,id,array, raiseFlag = True):
        """
            Deactivates module found by ID.
            :param cls: Module
            :param id: Integer or None
            :param array: Data to update in array (updates what is included, rest is left untouched)
            :param raiseFlag: If True and Module not found raises DbException
        """
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
        """
            Creates or updates module by ID.
            :param cls: Module
            :param id: Integer or None
            :param project_id: Id of project which module is part of
            :param name: Name of moduleId
            :param created: Timestamp of creation
            :param update: Timestamp of last update
            :param active: Used for deleting/deactivating module (Bool, True by default)
            :param data: Modue data (text.md)
            :param raiseFlag: If True and Module not found raises DbException
        """
        module = None
        if(id is not None):
            module = cls.get_module_by_id(id, False)
        if (module == None):
            res = cls.create_module(project_id, name, created, update, active, data, raiseFlag)
            return res
        if (module.project_id != project_id and project_id != None):
            if(data == None):
                data = module.get_data()
            res = cls.create_module(project_id, name, created, update, active, data, raiseFlag)
            return res
        changed = 0
        if (name != None):
            m = cls.get_module_by_name(name,False)
            if (m != None):
                if (m.id != id):
                    if raiseFlag:
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
        if (update != None):
            changed = 0
            module.update = update
            db.session.commit()
            if (data != None):
                #save "data"
                with open(os.path.dirname(__file__) + '/../../data/module/' + 
                          str(module.project_id) + '/' + str(module.id) + '.md', 'w') as f:
                    f.write(data)
            return module
        if (changed == 1):
            module.update = datetime.datetime.utcnow()
            db.session.commit()
            if (data != None):
                #save "data"
                with open(os.path.dirname(__file__) + '/../../data/module/' + 
                          str(module.project_id) + '/' + str(module.id) + '.md', 'w') as f:
                    f.write(data)
            return module
        return None

    @classmethod
    def create_module(cls, project_id=None, name=None, created=None, update=None, active=True, data=None, raiseFlag = True):
        """
            Creates module.
            :param cls: Module
            :param project_id: Id of project which module is part of
            :param name: Name of moduleId
            :param created: Timestamp of creation
            :param update: Timestamp of last update
            :param active: Used for deleting/deactivating module (Bool, True by default)
            :param data: Modue data (text.md)
            :param raiseFlag: If True and Module not found raises DbException
        """
        if (None != cls.get_module_by_name(name,False)):
            if raiseFlag:
                raise DbException(400, "Name is already taken.")
            return None
        if (None == Project.get_project_by_id(project_id, False)):
            if raiseFlag:
                raise DbException(404, "Project not found.")
            return None
        entity = Module(project_id=project_id, name=name, created=created, update=update, active=active)
        entity.save_entity()
        #save "data"
        if data != None:
            with open(os.path.dirname(__file__) + '/../../data/module/' + 
                      str(entity.project_id) + '/' + str(entity.id) + '.md', 'w') as f:
                f.write(data)
        return entity

    @staticmethod
    def find_str(text, looking_for):
        """
            Tries to find string within text if it succeeds returns index.
            :param text: Text being searched through
            :param looking_for: Text you are trying to find
        """
        i = 0

        if looking_for in text:
            c = looking_for[0]
            for ch in text:
                if ch == c:
                    if text[i:i+len(looking_for)] == looking_for:
                        return i

                i += 1

        return -1

    def build_module(self, passed_files = [], raiseFlag = True):
        """
            Builds module.
            :param self: Instance of Module class
            :param passed_files: Modules already used
            :param raiseFlag: If raiseFlag and modules are in cycle raises DbException
        """
        module_id = self.id
        
        if module_id in passed_files:
            if raiseFlag:
                raise DbException(400, 'Module ' + module_id + ' is in cycle.')
            return ''
        
        passed_files.append(module_id)
        with open(os.path.dirname(__file__) + '/../../data/module/' +
                  str(self.project_id) + '/' + str(module_id) + '.md' , 'r') as f:
            data = f.read()
        out_string = ''
        index1=0
        index2=0
        while (True):
            index1 = Module.find_str(data, '[[')
            index2 = Module.find_str(data[index1:], ']]')
            if (index1==-1 or index2==-1):
                break
            out_string+=data[:index1]
            module = Module.get_module_by_id(data[index1+2:index1 + index2])
            out_string+=module.build_module(passed_files, raiseFlag)
#            tmp=module.build_module(passed_files, raiseFlag)
#            out_string+=tmp[:len(tmp)-1]
            data=data[index1+index2+2:]
        out_string+=data
        passed_files.remove(module_id)
        return out_string

