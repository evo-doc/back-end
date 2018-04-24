"""User: Contains all entities that are related to permissions
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, desc
from evodoc.app import db


class ModulePerm (db.Model):
    __tablename__ = "module_perm"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    module_id = Column(Integer)
    permissions = Column(Integer) #8=owner, 4=write, 2=read -up for discussion

    def __init__(self, user_id=None, module_id=None, permissions=None):
        self.user_id=user_id
        self.module_id=module_id
        self.permissions=permissions

    def __repr__(self):
        return "<ModulePermission %r>" % (self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'permissions': self.permissions
        }

    def get_module_perm_by_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_module_perm_by_user_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(user_id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_module_perm_by_module_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(module_id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_module_perm_all(self, raiseFlag = True):
        perm = self.query.all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_module_perm_all_by_user_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(user_id=permId).all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_module_perm_all_by_module_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(module_id=permId).all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def update_module_perm_by_id(self, id, perm, raiseFlag = True):
        tmp = self.get_module_perm_all_by_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        tmp.update = datetime.datetime.utcnow
        db.session.commit()
        return True

    def update_module_perm_by_user_id(self, id, perm, raiseFlag = True):
        tmp = self.get_module_perm_all_by_user_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        db.session.commit()
        return True

    def update_module_perm_by_module_id(self, id, perm, raiseFlag = True):
        tmp = self.get_module_perm_all_by_module_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        db.session.commit()
        return True



class ProjectPerm (db.Model):
    __tablename__ = "project_perm"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    project_id = Column(Integer)
    permissions = Column(Integer) #8=owner, 4=write, 2=read -up for discussion

    def __init__(self, user_id=None, project_id=None, permissions=None):
        self.user_id=user_id
        self.project_id=project_id
        self.permissions=permissions

    def __repr__(self):
        return "<ProjectPermission %r>" % (self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.module_id,
            'permissions': self.permissions
        }

    def get_project_perm_by_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_project_perm_by_user_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(user_id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_project_perm_by_project_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(project_id=permId).first()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_project_perm_all(self, raiseFlag = True):
        perm = self.query.all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_project_perm_all_by_user_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(user_id=permId).all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def get_project_perm_all_by_project_id(self, permId, raiseFlag = True):
        perm = self.query.filter_by(project_id=permId).all()
        if (perm == None) & raiseFlag:
            raise DbException(DbException, 404, "Permission not found.")
        return perm

    def update_project_perm_by_id(self, id, perm, raiseFlag = True):
        tmp = self.get_project_perm_all_by_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        tmp.update = datetime.datetime.utcnow
        db.session.commit()
        return True

    def update_project_perm_by_user_id(self, id, perm, raiseFlag = True):
        tmp = self.get_project_perm_all_by_user_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        db.session.commit()
        return True

    def update_project_perm_by_project_id(self, id, perm, raiseFlag = True):
        tmp = self.get_project_perm_all_by_project_id(id,raiseFlag)
        if (tmp == None):
            return False
        tmp.permission = perm
        db.session.commit()
        return True
