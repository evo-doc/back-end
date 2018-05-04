import pytest
from evodoc import DbException
from evodoc.entity import User, UserType

userList = []

class TestUser:
    def prepare_user_data(self, session):
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
        userList.append(user)

    def test_get_user_by_id(self, session):
        """Test method get_user_by_id in User"""
        self.prepare_user_data(session)
        #Test something that really shouldn't be there
        with pytest.raises(DbException) as err:
            User.get_user_by_id(0)
        assert str(err.value) == "(404, 'User not found.')"

        user = User.get_user_by_id(userList[0].id)

        assert user.id == userList[0].id


