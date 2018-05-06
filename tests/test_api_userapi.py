import pytest, uuid
from datetime import datetime, timedelta
from flask import url_for
from evodoc.entity import User, UserToken, UserType

@pytest.mark.usefixture("session")
class TestUserapi:
    user_list = []
    token_list = []
    user_type_list = []

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
            self.user_type_list.append(user_type)
            session.add(user_type)
            session.commit()

        user = User("Admin", "admin@nimda.exp", "SuperSecret", None, None, True)
        user.user_type_id = UserType.get_type_by_name('ADMIN').id
        user.activated = True
        session.add(user)
        ttoken = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=ttoken).count() != 0) :
            ttoken = str(user.id).zfill(10) + str(uuid.uuid4())

        ttoken = UserToken(user_id=user.id,token=ttoken)
        ttoken.update = datetime.utcnow()
        ttoken.created = datetime.utcnow()
        session.add(ttoken)
        self.token_list.append(ttoken)
        self.user_list.append(user)
        session.commit()
        user = User("Test", "te@te.exp", "SuperSecret", None, None, True)
        session.add(user)
        session.commit()
        self.user_list.append(user)

        yield
        session.query(User).delete()
        session.query(UserType).delete()
        session.query(UserToken).delete()
        session.commit()
        self.user_list = []
        self.token_list = []
        self.user_type_list = []

    def test_get_user_by_id_action(self, session, client):
        """
        Test for GET method for user
        """
        token = self.token_list[0].token
        result = client.get(url_for('user.get_user_by_id_action') + "?token=" + token)
        result_data = result.get_json()
        assert result is not None
        assert result.status == "404 NOT FOUND"
        assert result_data == "User not found."

        result = client.get(url_for('user.get_user_by_id_action') + "?token=" + token + "&user_id=" + str(self.user_list[0].id))
        result_data = result.get_json()
        assert result is not None
        assert 'name' in result_data
        assert 'email' in result_data
        assert 'id' in result_data
        assert result_data['id'] == self.user_list[0].id

        result = client.get(url_for('user.get_user_by_id_action') + "?user_id=" + str(self.user_list[0].id))
        result_data = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_data == "Invalid token."

