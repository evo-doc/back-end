import pytest
import unittest
import datetime
from evodoc import DbException, create_app
from evodoc.entity import Project, db as _db

@pytest.mark.usefixture("session")
class TestProject():
    projectList = []

    @pytest.fixture(autouse = True)
    def setup(self, session):
        """
        SETUP funcion for TestProject class, this function is executed for each function in this TestClass
        """
        #make initial project
        session.add(Project('DummyProject_01'))
        session.commit()

        self.projectList = Project.query.all()

        yield
        session.query(Project).delete()
        session.commit()
        self.projectList[:] = []

    def test_get_project_by_id(self):
        """Test method get_project_by_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Project.get_project_by_id(0)
        assert str(err.value) == "(404, 'Project not found.')"

        project = Project.get_project_by_id(self.projectList[0].id)
        assert project.id == self.projectList[0].id
        assert project.name == self.projectList[0].name

        assert Project.get_project_by_id(0, False) == None

    def test_get_project_by_name(self):
        """Test method get_project_by_name in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Project.get_project_by_name('@')
        assert str(err.value) == "(404, 'Project not found.')"

        project = Project.get_project_by_name(self.projectList[0].name)
        assert project.id == self.projectList[0].id
        assert project.name == self.projectList[0].name

        assert Project.get_project_by_name('@', False) == None

    def test_get_project_all(self, session):
        """Test method get_project_all in User"""

        projects = Project.get_project_all()
        assert len(projects) == len(self.projectList)
        assert projects[0].id==self.projectList[0].id
        assert projects[0].name==self.projectList[0].name

        project = Project('DummyProject_02')
        session.add(project)
        session.commit()
        self.projectList.append(project)

        projects = Project.get_project_all()
        assert len(projects) == len(self.projectList)

        
        session.query(Project).delete()
        session.commit()

        projects = Project.get_project_all(False)
        assert projects == []

    def test_activate_project_by_id(self):
        """Test method activate_project_by_id & deactivate_project_by_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Project.activate_project_by_id(0)
        assert str(err.value) == "(404, 'Project not found.')"
        with pytest.raises(DbException) as err:
            Project.deactivate_project_by_id(0)
        assert str(err.value) == "(404, 'Project not found.')"

        Project.deactivate_project_by_id(self.projectList[0].id)
        project = Project.get_project_by_id(self.projectList[0].id)
        assert not project.active

        Project.activate_project_by_id(self.projectList[0].id)
        project = Project.get_project_by_id(self.projectList[0].id)
        assert project.active

        assert not Project.deactivate_project_by_id(0, False)
        assert not Project.activate_project_by_id(0, False)

    def test_create_project(self):
        """Test method create_project in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Project.create_project('DummyProject_01')
        assert str(err.value) == "(400, 'Name is already taken.')"

        project1 = Project.create_project('DummyProject_02')
        project2 = Project.get_project_by_id(project1.id)
        assert project1.id == project2.id
        assert project1.name == project2.name

        assert Project.create_project('DummyProject_02', raiseFlag = False) == None

    def test_create_project(self):
        """Test method update_project_by_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            Project.update_project_by_id(0)
        assert str(err.value) == "(404, 'Project not found.')"

        project1 = Project.create_project('DummyProject_02')

        with pytest.raises(DbException) as err:
            Project.update_project_by_id(self.projectList[0].id, 'DummyProject_02')
        assert str(err.value) == "(400, 'Name is already taken.')"

        project = Project.update_project_by_id(self.projectList[0].id, 'DummyProject_03')
        assert project.name=='DummyProject_03'
        assert Project.get_project_by_id(self.projectList[0].id).name=='DummyProject_03'

        created = datetime.datetime.utcnow() + datetime.timedelta(hours=-2)
        update = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)
        project = Project.update_project_by_id(self.projectList[0].id, 'dummy', created, update, False)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy'
        assert project.created == created
        assert project.update == update
        assert project.active == False

        project = Project.update_project_by_id(self.projectList[0].id, 'dummy', active=True)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy'
        assert project.created == created
        assert project.update > update
        assert project.active == True

        assert Project.update_project_by_id(0, raiseFlag = False) == None

    def test_create_or_update_project_by_id(self):
        """Test method create_or_update_project_by_id in User"""
        project1 = Project.create_or_update_project_by_id(None ,'DummyProject_02')
        with pytest.raises(DbException) as err:
            Project.create_or_update_project_by_id(self.projectList[0].id, 'DummyProject_02')
        assert str(err.value) == "(400, 'Name is already taken.')"

        project = Project.create_or_update_project_by_id(self.projectList[0].id, 'DummyProject_03')
        assert project.name=='DummyProject_03'
        assert Project.get_project_by_id(self.projectList[0].id).name=='DummyProject_03'

        created = datetime.datetime.utcnow() + datetime.timedelta(hours=-2)
        update = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)
        project = Project.create_or_update_project_by_id(self.projectList[0].id, 'dummy', created, update, False)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy'
        assert project.created == created
        assert project.update == update
        assert project.active == False

        project = Project.create_or_update_project_by_id(self.projectList[0].id, 'dummy', active=True)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy'
        assert project.created == created
        assert project.update > update
        assert project.active == True

        assert Project.create_or_update_project_by_id(0,'dummy', raiseFlag = False) == None

    def test_create_or_update_project_by_id_array(self):
        """Test method create_or_update_project_by_id_array in User"""
        array = {'name':'DummyProject_02'}
        
        project1 = Project.create_or_update_project_by_id_array(None ,array)
        with pytest.raises(DbException) as err:
            Project.create_or_update_project_by_id_array(self.projectList[0].id, array)
        assert str(err.value) == "(400, 'Name is already taken.')"

        array = {'name':'DummyProject_03'}
        project = Project.create_or_update_project_by_id_array(self.projectList[0].id, array)
        assert project.name=='DummyProject_03'
        assert Project.get_project_by_id(self.projectList[0].id).name=='DummyProject_03'

        created = datetime.datetime.utcnow() + datetime.timedelta(hours=-2)
        update = datetime.datetime.utcnow() + datetime.timedelta(hours=-1)
        array = {'name':'dummy',
                 'created':created,
                 'update':update,
                 'active':False}
        project = Project.create_or_update_project_by_id_array(self.projectList[0].id, array)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy'
        assert project.created == created
        assert project.update == update
        assert project.active == False

        array = {'name':'dummy',
                 'active':True}
        project = Project.create_or_update_project_by_id_array(self.projectList[0].id, array)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy'
        assert project.created == created
        assert project.update > update
        assert project.active == True

        array = {'name':'dummy2',
                 'kek':'kek'}
        project = Project.create_or_update_project_by_id_array(self.projectList[0].id, array)
        assert project.id ==Project.get_project_by_id(self.projectList[0].id).id
        assert project.name == 'dummy2'
        assert project.created == created
        assert project.update > update
        assert project.active == True

        array = {'name':'dummy2'}
        assert Project.create_or_update_project_by_id_array(0, array, raiseFlag=False)==None







