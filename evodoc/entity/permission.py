"""User: Contains all entities that are related to permissions
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
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
	 
	 
