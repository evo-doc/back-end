"""User: Contains all entities that are related to permissions
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, desc
from evodoc.entity import db
from evodoc.entity.module import Module
from evodoc.entity.user import User
from evodoc import DbException


class ModulePerm (db.Model):
    __tablename__ = "module_perm"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    module_id = Column(Integer, ForeignKey("module.id"))
    permissions = Column(Integer)
    """
        1 - Read
        2 - Write
        4 - Share
        8 - Own
    """

    def __init__(self, user_id=None, module_id=None, permissions=None):
        self.user_id=user_id
        self.module_id=module_id
        self.permissions=permissions

    def __repr__(self):
        return "<ModulePermission %r>" % (self.id)

    def serialize(self):
        """
        Serialize object for json
            :param self:
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'permissions': self.permissions
        }

    @classmethod
    def get_module_perm_by_id(cls, permId, raiseFlag = True):
        """
            Returns module found by ID.
            :param cls: ModulePerm
            :param permId: ID of ModulePerm class
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.query.filter_by(id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(404, "Permission not found.")
        return perm

#    @classmethod
#    def get_module_perm_by_user_id(cls, permId, raiseFlag = True):
#        perm = cls.query.filter_by(user_id=permId).first()
#        if (perm == None) & raiseFlag:
#            raise DbException(DbException, 404, "Permission not found.")
#        return perm

#    @classmethod
#    def get_module_perm_by_module_id(cls, permId, raiseFlag = True):
#        perm = cls.query.filter_by(module_id=permId).first()
#        if (perm == None) & raiseFlag:
#            raise DbException(DbException, 404, "Permission not found.")
#        return perm

    @classmethod
    def get_module_perm_by_user_and_module_id(cls, user_id, module_id, raiseFlag = True):
        """
            Returns module permission found by user_id and module_id.
            :param cls: ModulePerm
            :param user_id: ID of User
            :param module_id: ID of Module
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.query.filter_by(module_id=module_id).filter_by(user_id=user_id).first()
        if (perm == None) & raiseFlag:
            raise DbException(404, "Permission not found.")
        return perm

    @classmethod
    def get_module_perm_all(cls, raiseFlag = True):
        """
            Returns all permissions for all modules.
            :param cls: ModulePerm
            :param user_id: ID of User
            :param module_id: ID of Module
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.query.all()
        if (perm == None or perm == []) & raiseFlag:
            raise DbException(404, "Permission not found.")
        return perm

    @classmethod
    def get_module_perm_all_by_user_id(cls, permId, raiseFlag = True):
        """
            Returns all permissions for one user.
            :param cls: ModulePerm
            :param permId: ID of User
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.query.filter_by(user_id=permId).all()
        if (perm == None or perm == []) & raiseFlag:
            raise DbException(404, "Permission not found.")
        return perm

    @classmethod
    def get_module_perm_all_by_module_id(cls, permId, raiseFlag = True):
        """
            Returns all permissions for one module.
            :param cls: ModulePerm
            :param permId: ID of Module
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.query.filter_by(module_id=permId).all()
        if (perm == None or perm == []) & raiseFlag:
            raise DbException(404, "Permission not found.")
        return perm

    @classmethod
    def update_module_perm_by_id(cls, id, perm, raiseFlag = True):
        """
            Updates permissions by ModulePerm ID.
            :param cls: ModulePerm
            :param id: ModulePerm ID
            :param perm: permission flag
            :param raiseFlag: If True and permission not found raises DbException
        """
        tmp = cls.get_module_perm_by_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permissions = perm
        db.session.commit()
        return True

    @classmethod
    def update_module_perm_by_user_and_module_id(cls,user_id,module_id,perm,raiseFlag=True):
        """
            Updates permission from combination of user and module id.
            :param cls: ModulePerm
            :param permId: ID of User
            :param raiseFlag: If True and permission not found raises DbException
        """
        tmp = cls.get_module_perm_by_user_and_module_id(user_id,module_id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permissions = perm
        db.session.commit()
        return True

#    @classmethod
#    def update_module_perm_by_user_id(cls, id, perm, raiseFlag = True):
#        tmp = cls.get_module_perm_all_by_user_id(id,raiseFlag)
#        if (tmp == None):
#            return False
#        tmp.permission = perm
#        db.session.commit()
#        return True

#    @classmethod
#    def update_module_perm_by_module_id(cls, id, perm, raiseFlag = True):
#        tmp = cls.get_module_perm_all_by_module_id(id,raiseFlag)
#        if (tmp == None):
#            return False
#        tmp.permission = perm
#        db.session.commit()
#        return True

    def check_perm_read_raw(self):
        """
            Returns True if read permission was assigned, otherwise False.
            :param self: Instance of ModulePerm class
        """
        if ((self.permissions & 1) is 1): return True
        return False

    def check_perm_write_raw(self):
        """
            Returns True if write permission was assigned, otherwise False.
            :param self: Instance of ModulePerm class
        """
        if ((self.permissions & 2) is 2): return True
        return False

    def check_perm_share_raw(self):
        """
            Returns True if share permission was assigned, otherwise False.
            :param self: Instance of ModulePerm class
        """
        if ((self.permissions & 4) is 4): return True
        return False

    def check_perm_own_raw(self):
        """
            Returns True if own permission was assigned, otherwise False.
            :param self: Instance of ModulePerm class
        """
        if ((self.permissions & 8) is 8): return True
        return False

    @classmethod
    def check_perm_read_by_user_and_module_id(cls, user_id, module_id, raiseFlag = True):
        """
            Returns True if read permission was assigned, otherwise False.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_read_raw()
        return False

    @classmethod
    def check_perm_write_by_user_and_module_id(cls, user_id, module_id, raiseFlag = True):
        """
            Returns True if write permission was assigned, otherwise False.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_write_raw()
        return False

    @classmethod
    def check_perm_share_by_user_and_module_id(cls, user_id, module_id, raiseFlag = True):
        """
            Returns True if share permission was assigned, otherwise False.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_share_raw()
        return False

    @classmethod
    def check_perm_own_by_user_and_module_id(cls, user_id, module_id, raiseFlag = True):
        """
            Returns True if own permission was assigned, otherwise False.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_own_raw()
        return False

    def save_entity(self):
        """
            Saves entity. Function is unguarded and its expected that all data being inserted are correct.
            :param self: Instance of ModulePerm class
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def give_perm_read_user_module_id_raw(cls, user_id, module_id, raiseFlag = True):
        """
            Gives user read permission to module.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, False)
        if (perm != None):
            perm.permissions = perm.permissions | 1
            db.session.commit()
            return True
        if (User.get_user_by_id(user_id, raiseFlag) == None): return False
        if (Module.get_module_by_id(module_id, raiseFlag) == None): return False
        
        perm = ModulePerm(user_id, module_id, 1)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_write_user_module_id_raw(cls, user_id, module_id, raiseFlag = True):
        """
            Gives user write permission to module.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, False)
        if (perm != None):
            perm.permissions = perm.permissions | 2
            db.session.commit()
            return True
        if (User.get_user_by_id(user_id, raiseFlag) == None): return False
        if (Module.get_module_by_id(module_id, raiseFlag) == None): return False
        
        perm = ModulePerm(user_id, module_id, 2)
        perm.save_entity()
        return True 

    @classmethod
    def give_perm_share_user_module_id_raw(cls, user_id, module_id, raiseFlag = True):
        """
            Gives user share permission to module.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, False)
        if (perm != None):
            perm.permissions = perm.permissions | 4
            db.session.commit()
            return True
        if (User.get_user_by_id(user_id, raiseFlag) == None): return False
        if (Module.get_module_by_id(module_id, raiseFlag) == None): return False
        
        perm = ModulePerm(user_id, module_id, 4)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_own_user_module_id_raw(cls, user_id, module_id, raiseFlag = True):
        """
            Gives user own permission to module.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_module_perm_by_user_and_module_id(user_id, module_id, False)
        if (perm != None):
            perm.permissions = perm.permissions | 8
            db.session.commit()
            return True
        if (User.get_user_by_id(user_id, raiseFlag) == None): return False
        if (Module.get_module_by_id(module_id, raiseFlag) == None): return False
        
        perm = ModulePerm(user_id, module_id, 8)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_read_guarded(cls, master_id, user_id, module_id, raiseFlag = True):
        """
            Gives user read permission to module.
            :param cls: ModulePerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param module_id: ID of module that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ModulePerm.check_perm_share_by_user_and_module_id(master_id, module_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ModulePerm.give_perm_read_user_module_id_raw(user_id, module_id, raiseFlag)

    @classmethod
    def give_perm_write_guarded(cls, master_id, user_id, module_id, raiseFlag = True):
        """
            Gives user read permission to module.
            :param cls: ModulePerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param module_id: ID of module that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ModulePerm.check_perm_share_by_user_and_module_id(master_id, module_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ModulePerm.give_perm_write_user_module_id_raw(user_id, module_id, raiseFlag)

    @classmethod
    def give_perm_share_guarded(cls, master_id, user_id, module_id, raiseFlag = True):
        """
            Gives user read permission to module.
            :param cls: ModulePerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param module_id: ID of module that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ModulePerm.check_perm_own_by_user_and_module_id(master_id, module_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ModulePerm.give_perm_share_user_module_id_raw(user_id, module_id, raiseFlag)

    @classmethod
    def give_perm_own_guarded(cls, master_id, user_id, module_id, raiseFlag = True):
        """
            Gives user read permission to module.
            :param cls: ModulePerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param module_id: ID of module that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ModulePerm.check_perm_own_by_user_and_module_id(master_id, module_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ModulePerm.give_perm_own_user_module_id_raw(user_id, module_id, raiseFlag)

    @classmethod
    def check_perm_read_include_project_perm(cls, user_id, module_id, raiseFlag = True):
        """
            Checks read permission including project permissions.
            :param cls: ModulePerm
            :param user_id:
            :param module_id:
            :param raiseFlag: If True and permission not found or insufficient raises DbException
        """
        if ((not ModulePerm.check_perm_read_by_user_and_module_id(user_id, module_id)) or 
            (not ProjectPerm.check_perm_read_by_user_and_project_id(
                                    user_id,
                                    Module.get_module_by_id(module_id).project_id
                                    ))):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return True

###############################################################################
class ProjectPerm (db.Model):
    __tablename__ = "project_perm"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))
    permissions = Column(Integer)
    """
        1 - Read
        2 - Write
        4 - Share
        8 - Own
    """

    def __init__(self, user_id=None, project_id=None, permissions=None):
        self.user_id=user_id
        self.project_id=project_id
        self.permissions=permissions

    def __repr__(self):
        return "<ProjectPermission %r>" % (self.id)

    def serialize(self):
        """
        Serialize object for json
            :param self:
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'permissions': self.permissions
        }

    @classmethod
    def get_project_perm_by_id(cls, permId, raiseFlag = True):
        """
            Returns ProjectPerm found by ID.
            :param cls: ProjectPerm
            :param permId:
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.query.filter_by(id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

#    @classmethod
#    def get_project_perm_by_user_id(cl, permId, raiseFlag = True):
#        perm = cls.query.filter_by(user_id=permId).first()
#        if (perm == None) & raiseFlag:
#            raise DbException(DbException, 404, "Permission not found.")
#        return perm

#    @classmethod
#    def get_project_perm_by_project_id(cls, permId, raiseFlag = True):
#        perm = self.query.filter_by(project_id=permId).first()
#        if (perm == None) & raiseFlag:
#            raise DbException(DbException, 404, "Permission not found.")
#        return perm

    @classmethod
    def get_project_perm_by_user_and_project_id(cls, user_id, project_id, raiseFlag = True):
        """
            Returns ProjectPerm found by user id and project id.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.query.filter_by(project_id=project_id).filter_by(user_id=user_id).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    @classmethod
    def get_project_perm_all(cls, raiseFlag = True):
        """
            Returns all ProjectPerm.
            :param cls: ProjectPerm
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.query.all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    @classmethod
    def get_project_perm_all_by_user_id(cls, permId, raiseFlag = True):
        """
            Returns all ProjectPerm for one user.
            :param cls: ProjectPerm
            :param permId: ID of user
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.query.filter_by(user_id=permId).all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    @classmethod
    def get_project_perm_all_by_project_id(cls, permId, raiseFlag = True):
        """
            Returns all ProjectPerm for one project.
            :param cls: ProjectPerm
            :param permId: ID of project
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.query.filter_by(project_id=permId).all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    @classmethod
    def update_project_perm_by_id(cls, id, perm, raiseFlag = True):
        """
            Updates permission flag for one project found by ProjectPerm ID.
            :param cls: ProjectPerm
            :param id: ProjectPerm
            :param perm: permission flag to be set
            :param raiseFlag: If True and permission not found raises DbException.
        """
        tmp = cls.get_project_perm_all_by_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        tmp.update = datetime.datetime.utcnow
        db.session.commit()
        return True

#    @classmethod
#    def update_project_perm_by_user_id(cls, id, perm, raiseFlag = True):
#        tmp = cls.get_project_perm_all_by_user_id(id,raiseFlag)
#        if (tmp == None):
#            return False
#        tmp.permission = perm
#        db.session.commit()
#        return True

#    @classmethod
#    def update_project_perm_by_project_id(cls, id, perm, raiseFlag = True):
#        tmp = cls.get_project_perm_all_by_project_id(id,raiseFlag)
#        if (tmp == None):
#            return False
#        tmp.permission = perm
#        db.session.commit()
#        return True

    def check_perm_read_raw(self):
        """
            Returns True if read permission was assigned, otherwise False.
            :param self: Instance of ProjectPerm class
        """
        if ((self.permissions & 1) is 1): return True
        return False

    def check_perm_write_raw(self):
        """
            Returns True if write permission was assigned, otherwise False.
            :param self: Instance of ProjectPerm class
        """
        if ((self.permissions & 2) is 2): return True
        return False

    def check_perm_share_raw(self):
        """
            Returns True if share permission was assigned, otherwise False.
            :param self: Instance of ProjectPerm class
        """
        if ((self.permissions & 4) is 4): return True
        return False

    def check_perm_own_raw(self):
        """
            Returns True if own permission was assigned, otherwise False.
            :param self: Instance of ProjectPerm class
        """
        if ((self.permissions & 8) is 8): return True
        return False

    @classmethod
    def check_perm_read_by_user_and_project_id(cls, user_id, project_id, raiseFlag = False):
        """
            Returns True if read permission was assigned, otherwise False.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_read_raw()
        return False

    @classmethod
    def check_perm_write_by_user_and_project_id(cls, user_id, project_id, raiseFlag = False):
        """
            Returns True if write permission was assigned, otherwise False.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_write_raw()
        return False

    @classmethod
    def check_perm_share_by_user_and_project_id(cls, user_id, project_id, raiseFlag = False):
        """
            Returns True if share permission was assigned, otherwise False.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_share_raw()
        return False

    @classmethod
    def check_perm_own_by_user_and_project_id(cls, user_id, project_id, raiseFlag = False):
        """
            Returns True if own permission was assigned, otherwise False.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException.
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, raiseFlag)
        if (perm != None):
            return perm.check_perm_own_raw()
        return False

    def save_entity(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def give_perm_read_user_project_id_raw(cls, user_id, project_id, raiseFlag = True):
        """
            Gives user read permission to project.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, False)
        if (perm != None):
            perm.permissions = perm.permissions & 1
            db.session.commit()
            return True
        perm = ProjectPerm(user_id, project_id, 1)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_write_user_project_id_raw(cls, user_id, project_id, raiseFlag = True):
        """
            Gives user write permission to project.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, False)
        if (perm != None):
            perm.permissions = perm.permissions & 2
            db.session.commit()
            return True
        perm = ProjectPerm(user_id, project_id, 2)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_share_user_project_id_raw(cls, user_id, project_id, raiseFlag = True):
        """
            Gives user share permission to project.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, False)
        if (perm != None):
            perm.permissions = perm.permissions & 4
            db.session.commit()
            return True
        perm = ProjectPerm(user_id, project_id, 4)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_own_user_project_id_raw(cls, user_id, project_id, raiseFlag = True):
        """
            Gives user own permission to project.
            :param cls: ProjectPerm
            :param user_id:
            :param project_id:
            :param raiseFlag: If True and permission not found raises DbException
        """
        perm = cls.get_project_perm_by_user_and_project_id(user_id, project_id, False)
        if (perm != None):
            perm.permissions = perm.permissions & 8
            db.session.commit()
            return True
        perm = ProjectPerm(user_id, project_id, 8)
        perm.save_entity()
        return True

    @classmethod
    def give_perm_read_guarded(cls, master_id, user_id, project_id, raiseFlag = True):
        """
            Gives user read permission to project.
            :param cls: ProjectPerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param project_id: ID of project that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ProjectPerm.check_perm_share_by_user_and_project_id(master_id, project_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ProjectPerm.give_perm_read_user_project_id_raw(user_id, project_id, raiseFlag)

    @classmethod
    def give_perm_write_guarded(cls, master_id, user_id, project_id, raiseFlag = True):
        """
            Gives user write permission to project.
            :param cls: ProjectPerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param project_id: ID of project that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ProjectPerm.check_perm_share_by_user_and_project_id(master_id, project_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ProjectPerm.give_perm_write_user_project_id_raw(user_id, project_id, raiseFlag)

    @classmethod
    def give_perm_share_guarded(cls, master_id, user_id, project_id, raiseFlag = True):
        """
            Gives user share permission to project.
            :param cls: ProjectPerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param project_id: ID of project that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ProjectPerm.check_perm_own_by_user_and_project_id(master_id, project_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ProjectPerm.give_perm_share_user_project_id_raw(user_id, project_id, raiseFlag)

    @classmethod
    def give_perm_own_guarded(cls, master_id, user_id, project_id, raiseFlag = True):
        """
            Gives user own permission to project.
            :param cls: ProjectPerm
            :param master_id: ID of user giving the permission
            :param user_id: ID of user geting permission
            :param project_id: ID of project that will be accessed
            :param raiseFlag: If True and permission not found raises DbException
        """
        if not (ProjectPerm.check_perm_own_by_user_and_project_id(master_id, project_id)):
            if raiseFlag:
                raise DbException(405, "Insufficient permission.")
            return False
        return ProjectPerm.give_perm_own_user_project_id_raw(user_id, project_id, raiseFlag)

