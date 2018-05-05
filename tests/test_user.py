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


