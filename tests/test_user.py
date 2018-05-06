import pytest
import unittest
from evodoc import DbException, create_app
from evodoc.entity import User, UserType, db as _db

@pytest.mark.usefixture("session")
class TestUser():
    userList = []

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

        user = User("Admin", "admin@nimda.exp", "SuperSecret", None, None, True)
        user.user_type_id = UserType.get_type_by_name('ADMIN').id
        user.activated = True
        session.add(user)
        session.commit()
        self.userList.append(user)
        yield
        session.query(User).delete()
        session.query(UserType).delete()
        session.commit()
        self.userList[:] = []

    def test_get_user_by_id(self):
        """Test method get_user_by_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_by_id(0)
        assert str(err.value) == "(404, 'User not found.')"

        user = User.get_user_by_id(self.userList[0].id)
        assert user.id == self.userList[0].id

        user = User.get_user_by_id(0, False)
        assert user is None

    def test_get_user_by_name(self):
        """Test method get_user_by_name in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_by_name('@')
        assert str(err.value) == "(404, 'User not found.')"

        user = User.get_user_by_name(self.userList[0].name)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name

        user = User.get_user_by_name('@', False)
        assert user is None

    def test_get_user_by_email(self):
        """Test method get_user_by_email in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_by_email('@')
        assert str(err.value) == "(404, 'User not found.')"

        user = User.get_user_by_email(self.userList[0].email)
        assert user.id == self.userList[0].id
        assert user.email == self.userList[0].email

        user = User.get_user_by_email('@', False)
        assert user is None

    def test_get_user_by_username_or_email(self):
        """Test method get_user_by_username_or_email in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_by_email('@')
        assert str(err.value) == "(404, 'User not found.')"

        user = User.get_user_by_username_or_email(self.userList[0].name)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name
        assert user.email == self.userList[0].email

        user = User.get_user_by_username_or_email(self.userList[0].email)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name
        assert user.email == self.userList[0].email

        user = User.get_user_by_email('@', False)   
        assert user is None

    def test_get_user_all(self, session):
        """Test method get_user_all in User"""

        users = User.get_user_all()
        assert len(users) == len(self.userList)
        assert users[0].id==self.userList[0].id
        assert users[0].name==self.userList[0].name
        assert users[0].email==self.userList[0].email
        assert users[0].password==self.userList[0].password

        user = User("DUMMY", "dummy@dummy.dummy", "hackPr00f", None, None, True)
        user.user_type_id = UserType.get_type_by_name('USER').id
        user.activated = True
        session.add(user)
        session.commit()
        self.userList.append(user)

        users = User.get_user_all()
        assert len(users) == len(self.userList)

        
        session.query(User).delete()
        session.commit()

        users = User.get_user_all(False)
        assert users == []

        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_all()
        assert str(err.value) == "(404, 'No user found.')"

    def test_get_user_all_by_user_type_id(self, session):
        """Test method get_user_all_by_user_type_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_all_by_user_type_id(UserType.get_type_by_name('USER').id)
        assert str(err.value) == "(404, 'No user found.')"

        with pytest.raises(DbException) as err:
            User.get_user_all_by_user_type_id(123)
        assert str(err.value) == "(404, 'No user found.')"

        users = User.get_user_all_by_user_type_id(UserType.get_type_by_name('ADMIN').id)
        assert len(users) == len(self.userList)
        assert users[0].id==self.userList[0].id
        assert users[0].name==self.userList[0].name
        assert users[0].email==self.userList[0].email
        assert users[0].password==self.userList[0].password

        user = User("DUMMY", "dummy@dummy.dummy", "hackPr00f", None, None, True)
        user.user_type_id = UserType.get_type_by_name('GUEST').id
        user.activated = True
        session.add(user)
        session.commit()
        self.userList.append(user)

        users = User.get_user_all_by_user_type_id(UserType.get_type_by_name('GUEST').id)
        assert users[0].id==self.userList[1].id
        assert users[0].name==self.userList[1].name
        assert users[0].email==self.userList[1].email
        assert users[0].password==self.userList[1].password

        users = User.get_user_all_by_user_type_id(UserType.get_type_by_name('USER').id, False)
        assert users == []

    def test_update_activation_by_id(self):
        """Test method update_activation_by_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.update_activation_by_id(0, False)
        assert str(err.value) == "(404, 'User not found.')"

        assert User.update_activation_by_id(self.userList[0].id, False)
        user = User.get_user_by_id(self.userList[0].id)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name
        assert user.email == self.userList[0].email
        assert user.activated == False

        assert User.update_activation_by_id(self.userList[0].id, True)
        user = User.get_user_by_id(self.userList[0].id)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name
        assert user.email == self.userList[0].email
        assert user.activated == True

        assert not User.update_activation_by_id(0, True, False)

    def test_activate_user_by_id(self):
        """Test method activate_user_by_id & deactivate_user_by_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.deactivate_user_by_id(0)
        assert str(err.value) == "(404, 'User not found.')"

        with pytest.raises(DbException) as err:
            User.activate_user_by_id(0)
        assert str(err.value) == "(404, 'User not found.')"

        assert User.deactivate_user_by_id(self.userList[0].id)
        user = User.get_user_by_id(self.userList[0].id)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name
        assert user.email == self.userList[0].email
        assert user.active == False

        assert User.activate_user_by_id(self.userList[0].id)
        user = User.get_user_by_id(self.userList[0].id)
        assert user.id == self.userList[0].id
        assert user.name == self.userList[0].name
        assert user.email == self.userList[0].email
        assert user.active == True

        assert not User.activate_user_by_id(0, False)
        assert not User.deactivate_user_by_id(0, False)

    def test_check_unique(self):
        """Test method check_unique in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.check_unique('Admin', '@', True)
        assert str(err.value) == "(400, 'username')"
        with pytest.raises(DbException) as err:
            User.check_unique('@', 'admin@nimda.exp', True)
        assert str(err.value) == "(400, 'email')"

        assert User.check_unique('@', '@')

        assert not User.check_unique('Admin', '@')
        assert not User.check_unique('@', 'admin@nimda.exp')

    def test_confirm_password(self):
        """Test method confirm_password in User"""
        user = User.get_user_by_id(self.userList[0].id)
        assert user.confirm_password('SuperSecret')
        assert not user.confirm_password('SuperSecret2')
        assert not user.confirm_password('SuperSecre2')
        assert not user.confirm_password('supersecret')
        assert not user.confirm_password('')
        assert not user.confirm_password('\\*\\"\"')

    def test_update_user_by_id_from_array(self, session):
        """Test method update_user_by_id_from_array in User"""
        array = {'name':'kektimusMaximusPrime',
                 'email':'kektimusMaximusPrime@kek.top',
                 'password':'passwd',
                 'user_type_id':2}

        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(0, array)
        assert str(err.value) == "(404, 'User not found.')"

        user = User("DUMMY", "dummy@dummy.dummy", "hackPr00f", None, None, True)
        user.user_type_id = UserType.get_type_by_name('GUEST').id
        user.activated = True
        session.add(user)
        session.commit()
        self.userList.append(user)

        assert len(self.userList)==2

        User.update_user_by_id_from_array(self.userList[1].id, array)
        user = User.get_user_by_id(self.userList[1].id)
        assert user.id==self.userList[1].id
        assert user.name=='kektimusMaximusPrime'
        assert user.email=='kektimusMaximusPrime@kek.top'
        assert user.confirm_password('passwd')
        assert user.user_type_id==2

        array = {}
        User.update_user_by_id_from_array(self.userList[1].id, array)
        user = User.get_user_by_id(self.userList[1].id)
        assert user.id==self.userList[1].id
        assert user.name=='kektimusMaximusPrime'
        assert user.email=='kektimusMaximusPrime@kek.top'
        assert user.confirm_password('passwd')
        assert user.user_type_id==2

        array = {'kek':123, 'token':'01235'}
        User.update_user_by_id_from_array(self.userList[1].id, array)
        user = User.get_user_by_id(self.userList[1].id)
        assert user.id==self.userList[1].id
        assert user.name=='kektimusMaximusPrime'
        assert user.email=='kektimusMaximusPrime@kek.top'
        assert user.confirm_password('passwd')
        assert user.user_type_id==2

        array = {'name':'kektimusMaximusPrime'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'username')"

        array = {'email':'kektimusMaximusPrime@kek.top'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'email')"

        array = {'user_type_id':2}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'usertype')"

        array = {'name':'kektimusMaximusPrime',
                 'password':'passwd'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'username')"
        assert not user.confirm_password('passwd')

        array = {'email':'kektimusMaximusPrime@kek.top',
                 'password':'passwd'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'email')"
        assert not user.confirm_password('passwd')

        array = {'user_type_id':2,
                 'password':'passwd'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'usertype')"
        assert not user.confirm_password('passwd')


