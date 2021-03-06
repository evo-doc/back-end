import pytest
import unittest
from evodoc import DbException, create_app
from evodoc.entity import User, UserType, UserToken, db as _db

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

        array = {'user_type_id':200}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'usertype')"

        array = {'name':'kektimusMaximusPrime',
                 'password':'passwd'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'username')"
        user = User.get_user_by_id(self.userList[0].id)
        assert not user.confirm_password('passwd')

        array = {'email':'kektimusMaximusPrime@kek.top',
                 'password':'passwd'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'email')"
        user = User.get_user_by_id(self.userList[0].id)
        assert not user.confirm_password('passwd')

        array = {'user_type_id':200,
                 'password':'passwd'}
        with pytest.raises(DbException) as err:
            User.update_user_by_id_from_array(self.userList[0].id, array)
        assert str(err.value) == "(400, 'usertype')"
        user = User.get_user_by_id(self.userList[0].id)
        assert not user.confirm_password('passwd')

    def test_get_user_type_from_user_id(self, session):
        """Test method get_user_type_from_user_id in User"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_type_from_user_id(0)
        assert str(err.value) == "(404, 'User not found.')"

        assert User.get_user_type_from_user_id(self.userList[0].id).id == self.userList[0].user_type_id
###############################################################################
"""
            USER TYPE
"""
###############################################################################
@pytest.mark.usefixture("session")
class TestUserType():
    typeList = []

    @pytest.fixture(autouse = True)
    def setup(self, session):
        """
        SETUP funcion for TestUserType class, this function is executed for each function in this TestClass
        """
        self.typeList.append(UserType("ADMIN", 2))
        self.typeList.append(UserType("GUEST", 0))
        self.typeList.append(UserType("USER", 1))

        user_type_db = UserType.query.all()

        for user in user_type_db:
            for seedUser in self.typeList:
                if (user.name == seedUser.name):
                    self.typeList.remove(seedUser)


        for user_type in self.typeList:
            session.add(user_type)
            session.commit()
        yield
        session.query(User).delete()
        session.query(UserType).delete()
        session.commit()
        self.typeList[:] = []

    def test_get_type_by_id(self):
        """Test method get_type_by_id in UserType"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            UserType.get_type_by_id(0)
        assert str(err.value) == "(404, 'UserType not found.')"

        userType = UserType.get_type_by_id(self.typeList[0].id)
        assert userType.id == self.typeList[0].id

        userType = UserType.get_type_by_id(0, False)
        assert userType is None

    def test_get_type_by_name(self):
        """Test method get_type_by_name in UserType"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            UserType.get_type_by_name('@')
        assert str(err.value) == "(404, 'UserType not found.')"

        userType = UserType.get_type_by_name(self.typeList[0].name)
        assert userType.name == self.typeList[0].name
        userType = UserType.get_type_by_name(self.typeList[1].name)
        assert userType.name == self.typeList[1].name
        userType = UserType.get_type_by_name(self.typeList[2].name)
        assert userType.name == self.typeList[2].name

        userType = UserType.get_type_by_name('@', False)
        assert userType is None

    def test_get_type_all(self, session):
        """Test method get_type_all in UserType"""
        assert len(UserType.get_type_all())==3
        session.add(UserType("dummy", 3))
        session.commit()
        assert len(UserType.get_type_all())==4

    def test_update_type_name_by_id(self, session):
        """Test method update_type_name_by_id in UserType"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            UserType.update_type_name_by_id(0, 'DUMMY')
        assert str(err.value) == "(404, 'UserType not found.')"

        assert UserType.update_type_name_by_id(self.typeList[0].id, 'DUMMY')
        userType = UserType.get_type_by_id(self.typeList[0].id)
        assert userType.name == 'DUMMY'

        assert not UserType.update_type_name_by_id(0, 'DUMMY', False)

    def test_update_type_permisson_by_id(self, session):
        """Test method update_type_permisson_by_id in UserType"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            UserType.update_type_permisson_by_id(0,3)
        assert str(err.value) == "(404, 'UserType not found.')"

        assert UserType.update_type_permisson_by_id(self.typeList[0].id, 3)
        userType = UserType.get_type_by_id(self.typeList[0].id)
        assert userType.permission_flag == 3

        assert not UserType.update_type_permisson_by_id(0, 3, False)

###############################################################################
"""
            TOKEN
"""
###############################################################################

@pytest.mark.usefixture("session")
class TestUserToken():
    userList = []
    tokenList = []

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
        token = UserToken(self.userList[0].id, 'token_placeholder')
        session.add(token)
        session.commit()
        self.tokenList.append(token)
        yield
        session.query(UserToken).delete()
        session.query(User).delete()
        session.query(UserType).delete()
        session.commit()
        self.tokenList[:] = []
        self.userList[:] = []

    def test_get_token_by_id(self):
        """Test method get_token_by_id in UserToken"""
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            UserToken.get_token_by_id(0)
        assert str(err.value) == "(404, 'UserToken not found.')"

        token = UserToken.get_token_by_id(self.tokenList[0].id)
        assert token.token == self.tokenList[0].token
        assert token.id == self.tokenList[0].id

        assert UserToken.get_token_by_id(0,False) == None

    def test_get_token_all(self, session):
        """Test method get_token_all in UserToken"""
        assert len(UserToken.get_token_all()) == 1
        token = UserToken(self.userList[0].id, 'token_placeholder2')
        session.add(token)
        session.commit()
        self.tokenList.append(token)
        assert len(UserToken.get_token_all()) == 2
        session.query(UserToken).delete()
        session.commit()
        self.tokenList[:] = []
        assert len(UserToken.get_token_all()) == 0

    def test_get_token_all_by_user_id(self, session):
        """Test method get_token_all_by_user_id in UserToken"""
        assert len(UserToken.get_token_all_by_user_id(self.userList[0].id)) == 1
        token = UserToken(self.userList[0].id, 'token_placeholder2')
        session.add(token)
        session.commit()
        self.tokenList.append(token)
        assert len(UserToken.get_token_all_by_user_id(self.userList[0].id)) == 2
        session.query(UserToken).delete()
        session.commit()
        self.tokenList[:] = []
        assert len(UserToken.get_token_all_by_user_id(self.userList[0].id, False)) == 0

        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            UserToken.get_token_all_by_user_id(0)
        assert str(err.value) == "(404, 'No userToken found.')"


