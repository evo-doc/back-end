import pytest
import unittest
import datetime
from evodoc import DbException, create_app
from evodoc.entity import Module, Project, db as _db

@pytest.mark.usefixture("session")
class TestModule():
    moduleList = []
    projectList = []

    @pytest.fixture(autouse = True)
    def setup(self, session):
        """
        SETUP funcion for TestModule class, this function is executed for each function in this TestClass
        """
        #make initial project
        session.add(Project.create_project('DummyProject_01'))
        session.add(Project.create_project('DummyProject_02'))
        session.commit()

        self.projectList = Project.query.all()

        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'M11'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'M12'))
        session.commit()

        self.moduleList = Module.query.all()

        yield
        session.query(Module).delete()
        session.query(Project).delete()
        session.commit()
        self.moduleList[:] = []
        self.projectList[:] = []

    def test_get_module_by_id(self):
        """Test method get_module_by_id in Module"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Module.get_module_by_id(0)
        assert str(err.value) == "(404, 'Module not found.')"

        module = Module.get_module_by_id(self.moduleList[0].id)
        assert module.id == self.moduleList[0].id
        assert module.name == self.moduleList[0].name

        assert Module.get_module_by_id(0, False) == None

    def test_get_module_by_name(self):
        """Test method get_module_by_name in Module"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Module.get_module_by_name('@')
        assert str(err.value) == "(404, 'Module not found.')"

        module = Module.get_module_by_name(self.moduleList[0].name)
        assert module.id == self.moduleList[0].id
        assert module.name == self.moduleList[0].name

        assert Module.get_module_by_name('@', False) == None

    def test_get_module_all(self, session):
        """Test method get_module_all in Module"""

        modules = Module.get_module_all()
        assert len(modules) == len(self.moduleList)
        assert modules[0].id==self.moduleList[0].id
        assert modules[0].name==self.moduleList[0].name

        module = Module(Project.get_project_by_name('DummyProject_01').id, 'M13')
        session.add(module)
        session.commit()
        self.moduleList.append(module)

        modules = Module.get_module_all()
        assert len(modules) == len(self.moduleList)

        
        session.query(Module).delete()
        session.commit()

        modules = Module.get_module_all(False)
        assert modules == []

    def test_get_module_all(self, session):
        """Test method get_module_all in Module"""

        modules = Module.get_module_all_by_project_id(Project.get_project_by_name('DummyProject_01').id)
        assert len(modules) == len(self.moduleList)
        assert modules[0].id==self.moduleList[0].id
        assert modules[0].name==self.moduleList[0].name

        module = Module(Project.get_project_by_name('DummyProject_01').id, 'M13')
        session.add(module)
        session.commit()
        self.moduleList.append(module)

        modules = Module.get_module_all_by_project_id(Project.get_project_by_name('DummyProject_01').id)
        assert len(modules) == len(self.moduleList)

        modules = Module.get_module_all_by_project_id(Project.get_project_by_name('DummyProject_02').id,False)
        assert modules == []

        session.query(Module).delete()
        session.commit()

        modules = Module.get_module_all_by_project_id(Project.get_project_by_name('DummyProject_01').id,False)
        assert modules == []

    def test_activate_module_by_id(self):
        """Test method activate_module_by_id & deactivate_module_by_id in Module"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Module.activate_module_by_id(0)
        assert str(err.value) == "(404, 'Module not found.')"
        with pytest.raises(DbException) as err:
            Module.deactivate_module_by_id(0)
        assert str(err.value) == "(404, 'Module not found.')"

        Module.deactivate_module_by_id(self.moduleList[0].id)
        module = Module.get_module_by_id(self.moduleList[0].id)
        assert not module.active

        Module.activate_module_by_id(self.moduleList[0].id)
        module = Module.get_module_by_id(self.moduleList[0].id)
        assert module.active

        assert not Module.deactivate_module_by_id(0, False)
        assert not Module.activate_module_by_id(0, False)

    def test_create_module(self):
        """Test method create_module in Module"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Module.create_module(0, 'M1111')
        assert str(err.value) == "(404, 'Project not found.')"
        with pytest.raises(DbException) as err:
            Module.create_module(Project.get_project_by_name('DummyProject_01').id, 'M11')
        assert str(err.value) == "(400, 'Name is already taken.')"

        created = datetime.datetime.utcnow() + datetime.timedelta(hours=-2)
        update = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)
        module = Module.create_module(Project.get_project_by_name('DummyProject_01').id,
                             name='M14', created=created, update=update, active=True,   
                             data='kektimusMaximusPrime', raiseFlag = True)

        assert module.project_id == Project.get_project_by_name('DummyProject_01').id
        assert module.name == 'M14'
        assert module.created == created
        assert module.update == update
        assert module.active == True
        assert module.get_data() == 'kektimusMaximusPrime'

        module = Module.create_module(Project.get_project_by_name('DummyProject_01').id,
                             name='M14', created=created, update=update, active=True,   
                             data='kektimusMaximusPrime', raiseFlag = False)
        assert module==None

        module = Module.create_module(1111111,
                             name='M15', created=created, update=update, active=True,   
                             data='kektimusMaximusPrime', raiseFlag = False)
        assert module==None

    def test_create_or_update_module_by_id(self):
        """Test method create_or_update_module_by_id in Module"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Module.create_or_update_module_by_id(0, 0, 'M1111')
        assert str(err.value) == "(404, 'Project not found.')"
        with pytest.raises(DbException) as err:
            Module.create_or_update_module_by_id(0, Project.get_project_by_name('DummyProject_01').id, 'M11')
        assert str(err.value) == "(400, 'Name is already taken.')"

        created = datetime.datetime.utcnow() + datetime.timedelta(hours=-2)
        update = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)
        module = Module.create_or_update_module_by_id(None, Project.get_project_by_name('DummyProject_01').id,
                             name='M14', created=created, update=update, active=True,   
                             data='kektimusMaximusPrime', raiseFlag = True)

        assert module.project_id == Project.get_project_by_name('DummyProject_01').id
        assert module.name == 'M14'
        assert module.created == created
        assert module.update == update
        assert module.active == True

        module = Module.create_or_update_module_by_id(module.id, Project.get_project_by_name('DummyProject_01').id,
                             name='M15', active=False, data='kektimusMaximusPrime',
                             raiseFlag = True)

        assert module.project_id == Project.get_project_by_name('DummyProject_01').id
        assert module.name == 'M15'
        assert module.created == created
        assert module.update > update
        assert module.active == False


        assert Module.create_or_update_module_by_id(0, 0, 'M1111', raiseFlag = False) == None
        assert Module.create_or_update_module_by_id(0, Project.get_project_by_name('DummyProject_01').id, 'M15', raiseFlag = False) == None

    def test_get_data(self):
        """Test method get_data in Module"""
        
        module = Module.create_or_update_module_by_id(Project.get_project_by_name('DummyProject_01').id, name='M15', active=False, data='kektimusMaximusPrime', raiseFlag = True)
        assert module.get_data() == 'kektimusMaximusPrime'


    def test_create_or_update_module_by_id_from_array(self):
        """Test method create_or_update_module_by_id_from_array in Module"""

        array = {'project_id': 0,
                 'name':'M1111'}

        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Module.create_or_update_module_by_id_from_array(0, array)
        assert str(err.value) == "(404, 'Project not found.')"

        array = {'project_id': Project.get_project_by_name('DummyProject_01').id,
                 'name':'M11'}

        with pytest.raises(DbException) as err:
            Module.create_or_update_module_by_id_from_array(0, array)
        assert str(err.value) == "(400, 'Name is already taken.')"

        created = datetime.datetime.utcnow() + datetime.timedelta(hours=-2)
        update = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)

        array = {'project_id': Project.get_project_by_name('DummyProject_01').id,
                 'name':'M14',
                 'created': created,
                 'update': update,
                 'active': True,
                 'data': 'kektimusMaximusPrime'}

        module = Module.create_or_update_module_by_id_from_array(None, array)

        assert module.project_id == Project.get_project_by_name('DummyProject_01').id
        assert module.name == 'M14'
        assert module.created == created
        assert module.update == update
        assert module.active == True

        array = {'project_id': Project.get_project_by_name('DummyProject_01').id,
                 'name':'M15',
                 'active': False,
                 'data': 'kektimusMaximusPrime'}

        module2 = Module.create_or_update_module_by_id_from_array(module.id, array)

        assert module2.project_id == Project.get_project_by_name('DummyProject_01').id
        assert module2.name == 'M15'
        assert module2.created == created
        assert module2.update > update
        assert module2.active == False

        array = {'project_id': 0,
                 'name':'M1111'}

        assert Module.create_or_update_module_by_id_from_array(0, array, raiseFlag=False) == None

        array = {'project_id': Project.get_project_by_name('DummyProject_01').id,
                 'name':'M15'}

        assert Module.create_or_update_module_by_id_from_array(0, array, raiseFlag=False) == None




