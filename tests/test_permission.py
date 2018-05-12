import pytest
import unittest
from evodoc import DbException, create_app
from evodoc.entity import User, UserType, UserToken, Project, Module, ModulePerm, ProjectPerm, db as _db

@pytest.mark.usefixture("session")
class TestModulePermission():
    moduleList = []
    projectList = []
    userList = []
    permList = []

    @pytest.fixture(autouse = True)
    def setup(self, session):
        """
        SETUP funcion for TestUser class, this function is executed for each function in this TestClass
        """
        user_types = []
        user_types.append(UserType("ADMIN", 2))
        user_types.append(UserType("GUEST", 0))
        user_types.append(UserType("USER", 1))

        user_type_db = UserType.query.all()

        for user in user_type_db:
            for seedUser in user_types:
                if (user.name == seedUser.name):
                    user_types.remove(seedUser)


        for user_type in user_types:
            session.add(user_type)
            session.commit()

        user = User("GUEST", "GUEST@nimda.exp", "GUEST", None, None, True)
        user.user_type_id = UserType.get_type_by_name('GUEST').id
        user.activated = True
        user1 = User("USER", "USER@nimda.exp", "USER", None, None, True)
        user1.user_type_id = UserType.get_type_by_name('USER').id
        user1.activated = True
        user2 = User("Admin", "admin@nimda.exp", "SuperSecret", None, None, True)
        user2.user_type_id = UserType.get_type_by_name('ADMIN').id
        user2.activated = True
        session.add(user)
        session.add(user1)
        session.add(user2)
        session.commit()
        self.userList.append(user)
        self.userList.append(user1)
        self.userList.append(user2)

        #make initial project
        session.add(Project.create_project('DummyProject_01'))
        session.add(Project.create_project('DummyProject_02'))
        session.commit()

        self.projectList = Project.query.all()

        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'M11'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'M12'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'M13'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'read'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'write'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'share'))
        session.add(Module(Project.get_project_by_name('DummyProject_01').id, 'own'))
        session.commit()

        self.moduleList = Module.query.all()

        perm0 = ModulePerm(self.userList[0].id, self.moduleList[0].id, 15)
        perm1 = ModulePerm(self.userList[0].id, self.moduleList[1].id, 8)
        perm2 = ModulePerm(self.userList[0].id, self.moduleList[2].id, 0)

        session.add(perm0)
        session.add(perm1)
        session.add(perm2)
        session.commit()

        self.permList.append(perm0)
        self.permList.append(perm1)
        self.permList.append(perm2)

        yield
        session.query(ModulePerm).delete()
        self.permList[:] = []

        session.query(Module).delete()
        session.query(Project).delete()
        session.commit()
        self.moduleList[:] = []
        self.projectList[:] = []

        session.query(User).delete()
        session.query(UserType).delete()
        session.commit()
        self.userList[:] = []

    def test_get_module_perm_by_id(self):
        """Test method get_module_perm_by_id in ModulePerm"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_by_id(0)
        assert str(err.value) == "(404, 'Permission not found.')"

        perm = ModulePerm.get_module_perm_by_id(self.permList[0].id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == self.permList[0].permissions

        assert ModulePerm.get_module_perm_by_id(0, False) == None

    def test_get_module_perm_by_user_and_module_id(self):
        """Test method get_module_perm_by_user_and_module_id in ModulePerm"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_by_user_and_module_id(0, 1)
        assert str(err.value) == "(404, 'Permission not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_by_user_and_module_id(1, 0)
        assert str(err.value) == "(404, 'Permission not found.')"

        perm = ModulePerm.get_module_perm_by_user_and_module_id(self.permList[0].user_id,   self.permList[0].module_id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == self.permList[0].permissions

        assert ModulePerm.get_module_perm_by_user_and_module_id(0, 1, False) == None
        assert ModulePerm.get_module_perm_by_user_and_module_id(1, 0, False) == None

    def test_get_module_perm_all(self, session):
        """Test method get_module_perm_all in ModulePerm"""

        perm = ModulePerm.get_module_perm_all()
        assert len(perm) == len(self.permList)

        session.query(ModulePerm).delete()
        session.commit()

        perm = ModulePerm.get_module_perm_all(False)
        assert len(perm) == 0
        assert perm == []

        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_all()
        assert str(err.value) == "(404, 'Permission not found.')"

    def test_get_module_perm_all_by_user_id(self, session):
        """Test method get_module_perm_all_by_user_id in ModulePerm"""

        perm = ModulePerm.get_module_perm_all_by_user_id(self.userList[0].id)
        assert len(perm) == len(self.permList)

        session.query(ModulePerm).delete()
        session.commit()

        perm = ModulePerm.get_module_perm_all_by_user_id(self.userList[0].id, False)
        assert len(perm) == 0
        assert perm == []

        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_all_by_user_id(self.userList[0].id)
        assert str(err.value) == "(404, 'Permission not found.')"

    def test_get_module_perm_all_by_module_id(self, session):
        """Test method get_module_perm_all_by_module_id in ModulePerm"""

        perm = ModulePerm.get_module_perm_all_by_module_id(self.moduleList[0].id)
        assert len(perm) == 1

        session.query(ModulePerm).delete()
        session.commit()

        perm = ModulePerm.get_module_perm_all_by_module_id(self.moduleList[0].id, False)
        assert len(perm) == 0
        assert perm == []

        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_all_by_module_id(self.moduleList[0].id)
        assert str(err.value) == "(404, 'Permission not found.')"

    def test_update_module_perm_by_id(self):
        """Test method update_module_perm_by_id in ModulePerm"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            ModulePerm.update_module_perm_by_id(0,0)
        assert str(err.value) == "(404, 'Permission not found.')"

        perm = ModulePerm.get_module_perm_by_id(self.permList[0].id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == self.permList[0].permissions

        assert ModulePerm.update_module_perm_by_id(self.permList[0].id, 11)
        perm = ModulePerm.get_module_perm_by_id(self.permList[0].id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == 11

        assert ModulePerm.get_module_perm_by_id(0, False) == None

    def test_update_module_perm_by_user_and_module_id(self):
        """Test method update_module_perm_by_user_and_module_id in ModulePerm"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            ModulePerm.update_module_perm_by_user_and_module_id(0, 1, 11)
        assert str(err.value) == "(404, 'Permission not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.update_module_perm_by_user_and_module_id(1, 0, 11)
        assert str(err.value) == "(404, 'Permission not found.')"

        perm = ModulePerm.get_module_perm_by_user_and_module_id(self.permList[0].user_id,   self.permList[0].module_id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == self.permList[0].permissions

        assert ModulePerm.update_module_perm_by_user_and_module_id(self.permList[0].user_id, self.permList[0].module_id, 11)

        perm = ModulePerm.get_module_perm_by_user_and_module_id(self.permList[0].user_id,   self.permList[0].module_id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == 11

        assert ModulePerm.update_module_perm_by_user_and_module_id(0, 1, 11, False) == False
        assert ModulePerm.update_module_perm_by_user_and_module_id(1, 0, 11, False) == False

    def test_check_perm(self):
        """Test method check_perm_read_raw, check_perm_write_raw, check_perm_share_raw and check_perm_own_raw in ModulePerm"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            ModulePerm.get_module_perm_by_id(0)
        assert str(err.value) == "(404, 'Permission not found.')"

        perm = ModulePerm.get_module_perm_by_id(self.permList[0].id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == self.permList[0].permissions
        assert perm.permissions == 15

        assert perm.check_perm_read_raw()
        assert perm.check_perm_write_raw()
        assert perm.check_perm_share_raw()
        assert perm.check_perm_own_raw()

        perm = ModulePerm.get_module_perm_by_id(self.permList[2].id)
        assert perm.id == self.permList[2].id
        assert perm.user_id == self.permList[2].user_id
        assert perm.module_id == self.permList[2].module_id
        assert perm.permissions == self.permList[2].permissions
        assert perm.permissions == 0

        assert not perm.check_perm_read_raw()
        assert not perm.check_perm_write_raw()
        assert not perm.check_perm_share_raw()
        assert not perm.check_perm_own_raw()

    def test_check_perm_by_user_and_module_id(self):
        """Test method check_perm_read_by_user_and_module_id, 
                       check_perm_write_by_user_and_module_id, 
                       check_perm_share_by_user_and_module_id and 
                       check_perm_own_by_user_and_module_id in ModulePerm"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_read_by_user_and_module_id(0, 1, True)
        assert str(err.value) == "(404, 'Permission not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_read_by_user_and_module_id(1, 0, True)
        assert str(err.value) == "(404, 'Permission not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_write_by_user_and_module_id(0, 1, True)
        assert str(err.value) == "(404, 'Permission not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_write_by_user_and_module_id(1, 0, True)
        assert str(err.value) == "(404, 'Permission not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_share_by_user_and_module_id(0, 1, True)
        assert str(err.value) == "(404, 'Permission not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_share_by_user_and_module_id(1, 0, True)
        assert str(err.value) == "(404, 'Permission not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_own_by_user_and_module_id(0, 1, True)
        assert str(err.value) == "(404, 'Permission not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.check_perm_own_by_user_and_module_id(1, 0, True)
        assert str(err.value) == "(404, 'Permission not found.')"

        assert not ModulePerm.check_perm_read_by_user_and_module_id(0, 1, False)
        assert not ModulePerm.check_perm_read_by_user_and_module_id(1, 0, False)
        assert not ModulePerm.check_perm_write_by_user_and_module_id(0, 1, False)
        assert not ModulePerm.check_perm_write_by_user_and_module_id(1, 0, False)
        assert not ModulePerm.check_perm_share_by_user_and_module_id(0, 1, False)
        assert not ModulePerm.check_perm_share_by_user_and_module_id(1, 0, False)
        assert not ModulePerm.check_perm_own_by_user_and_module_id(0, 1, False)
        assert not ModulePerm.check_perm_own_by_user_and_module_id(1, 0, False)

        perm = ModulePerm.get_module_perm_by_id(self.permList[0].id)
        assert perm.id == self.permList[0].id
        assert perm.user_id == self.permList[0].user_id
        assert perm.module_id == self.permList[0].module_id
        assert perm.permissions == self.permList[0].permissions
        assert perm.permissions == 15


        assert ModulePerm.check_perm_read_by_user_and_module_id(self.permList[0].user_id, self.permList[0].module_id)
        assert ModulePerm.check_perm_write_by_user_and_module_id(self.permList[0].user_id, self.permList[0].module_id)
        assert ModulePerm.check_perm_share_by_user_and_module_id(self.permList[0].user_id, self.permList[0].module_id)
        assert ModulePerm.check_perm_own_by_user_and_module_id(self.permList[0].user_id, self.permList[0].module_id)

        perm = ModulePerm.get_module_perm_by_id(self.permList[2].id)
        assert perm.id == self.permList[2].id
        assert perm.user_id == self.permList[2].user_id
        assert perm.module_id == self.permList[2].module_id
        assert perm.permissions == self.permList[2].permissions
        assert perm.permissions == 0

        assert not ModulePerm.check_perm_read_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert not ModulePerm.check_perm_write_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert not ModulePerm.check_perm_share_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert not ModulePerm.check_perm_own_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)

    def test_save_entity(self):
        """Test method update_module_perm_by_id in ModulePerm"""
        #Test something that really shouldn't be there
        perm = ModulePerm(self.userList[0].id, self.moduleList[3].id, 0)
        perm.save_entity()  

        perm1 = ModulePerm.get_module_perm_by_id(perm.id)
        assert perm.id == perm1.id
        assert perm1.permissions == 0

    def test_give_permssions_raw(self):
        """Test method give_perm_read_user_module_id_raw, 
                       give_perm_write_user_module_id_raw, 
                       give_perm_share_user_module_id_raw and 
                       give_perm_own_user_module_id_raw in ModulePerm"""
        #Test something that really shouldn't be there
        #non existent user or module
        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_read_user_module_id_raw(0, 1)
        assert str(err.value) == "(404, 'User not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_read_user_module_id_raw(1, 0)
        assert str(err.value) == "(404, 'Module not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_write_user_module_id_raw(0, 1)
        assert str(err.value) == "(404, 'User not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_write_user_module_id_raw(1, 0)
        assert str(err.value) == "(404, 'Module not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_share_user_module_id_raw(0, 1)
        assert str(err.value) == "(404, 'User not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_share_user_module_id_raw(1, 0)
        assert str(err.value) == "(404, 'Module not found.')"

        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_own_user_module_id_raw(0, 1)
        assert str(err.value) == "(404, 'User not found.')"
        with pytest.raises(DbException) as err:
            ModulePerm.give_perm_own_user_module_id_raw(1, 0)
        assert str(err.value) == "(404, 'Module not found.')"

        #nonexistent user or module without flag
        assert not ModulePerm.give_perm_read_user_module_id_raw(0, 1, False)
        assert not ModulePerm.give_perm_read_user_module_id_raw(1, 0, False)
        assert not ModulePerm.give_perm_write_user_module_id_raw(0, 1, False)
        assert not ModulePerm.give_perm_write_user_module_id_raw(1, 0, False)
        assert not ModulePerm.give_perm_share_user_module_id_raw(0, 1, False)
        assert not ModulePerm.give_perm_share_user_module_id_raw(1, 0, False)
        assert not ModulePerm.give_perm_own_user_module_id_raw(0, 1, False)
        assert not ModulePerm.give_perm_own_user_module_id_raw(1, 0, False)

        perm = ModulePerm.get_module_perm_by_id(self.permList[2].id)
        assert perm.id == self.permList[2].id
        assert perm.user_id == self.permList[2].user_id
        assert perm.module_id == self.permList[2].module_id
        assert perm.permissions == self.permList[2].permissions
        assert perm.permissions == 0

        #user and module exists and have permission flag 0
        assert not ModulePerm.check_perm_read_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.give_perm_read_user_module_id_raw(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.check_perm_read_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)

        assert not ModulePerm.check_perm_write_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.give_perm_write_user_module_id_raw(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.check_perm_write_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)

        assert not ModulePerm.check_perm_share_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.give_perm_share_user_module_id_raw(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.check_perm_share_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)

        assert not ModulePerm.check_perm_own_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.give_perm_own_user_module_id_raw(self.permList[2].user_id, self.permList[2].module_id)
        assert ModulePerm.check_perm_own_by_user_and_module_id(self.permList[2].user_id, self.permList[2].module_id)

        #user and module exists but permission flag was not yet made 
        assert not ModulePerm.check_perm_read_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('read').id, False)
        assert ModulePerm.give_perm_read_user_module_id_raw(self.permList[2].user_id, Module.get_module_by_name('read').id)
        assert ModulePerm.check_perm_read_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('read').id)

        assert not ModulePerm.check_perm_write_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('write').id, False)
        assert ModulePerm.give_perm_write_user_module_id_raw(self.permList[2].user_id, Module.get_module_by_name('write').id)
        assert ModulePerm.check_perm_write_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('write').id)

        assert not ModulePerm.check_perm_share_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('share').id, False)
        assert ModulePerm.give_perm_share_user_module_id_raw(self.permList[2].user_id, Module.get_module_by_name('share').id)
        assert ModulePerm.check_perm_share_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('share').id)

        assert not ModulePerm.check_perm_own_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('own').id, False)
        assert ModulePerm.give_perm_own_user_module_id_raw(self.permList[2].user_id, Module.get_module_by_name('own').id)
        assert ModulePerm.check_perm_own_by_user_and_module_id(self.permList[2].user_id, Module.get_module_by_name('own').id)

