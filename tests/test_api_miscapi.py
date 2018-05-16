import pytest, uuid, json
from flask import url_for
from datetime import datetime, timedelta
from evodoc import DbException, ApiException
from evodoc.entity import User, UserType, UserToken

@pytest.mark.usefixture("session")
class TestMiscapi:
    user_list = []
    token_list = []

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
        self.user_list.append(user.id)
        user = User("Test", "te@te.exp", "SuperSecret", None, None, True)
        session.add(user)
        session.commit()
        self.user_list.append(user.id)

        yield
        session.query(User).delete()
        session.query(UserType).delete()
        session.query(UserToken).delete()
        session.commit()
        self.user_list = []
        self.token_list = []

    def test_login_action(self, session, client):
        """
        Integration test for login
        """
        data = {"username": "Admin", "password": "SuperSecret"}
        result = client.post(url_for('miscapi.login_action'), json = data)
        result_data = result.get_json()
        assert result_data != None
        assert result_data['verified'] == "true"
        user_id = self.user_list[0]
        token_from_db = UserToken.query.filter_by(user_id = user_id).order_by(UserToken.id.desc()).first()
        assert token_from_db != None
        assert result_data['token'] == token_from_db.token

        data["username"] = "ThisDoesNotExist"
        result = client.post(url_for('miscapi.login_action'), json = data)
        result_data = result.get_json()
        assert result.status == "400 BAD REQUEST"
        assert result_data == "userpass"

        data["username"] = "Admin"
        data["password"] = "YouShallNotPass"
        result = client.post(url_for('miscapi.login_action'), json = data)
        result_data = result.get_json()
        assert result.status == "400 BAD REQUEST"
        assert result_data == "userpass"

        result = client.post(url_for('miscapi.login_action'), json = {})
        result_data = result.get_json()
        assert result.status == "400 BAD REQUEST"
        assert result_data == "data"

        data["username"] = "Test"
        data["password"] = "SuperSecret"
        result = client.post(url_for('miscapi.login_action'), json = data)
        result_data = result.get_json()
        user_id = self.user_list[1]
        token_from_db = UserToken.query.filter_by(user_id = user_id).order_by(UserToken.id.desc()).first()
        assert token_from_db != None
        assert result.status == "200 OK"
        assert result_data['verified'] == "false" and result_data['token'] == token_from_db.token

    def test_registration_action(self, session, client):
        data = {
            "username": "newTestUser",
            "email": "example@test.com",
            "password": "Just&1Test"
        }
        result = client.post(url_for('miscapi.registration_action'), json = data)
        result_data = result.get_json()
        assert result_data != None
        assert result_data['user_id'] != 0
        user_id = result_data['user_id']
        token_from_db = UserToken.query.filter_by(user_id = user_id).order_by(UserToken.id.desc()).first()
        assert result_data['token'] == token_from_db.token

        result = client.post(url_for('miscapi.registration_action'), json = data)
        result_data = result.get_json()
        assert result_data != None
        assert result.status == "400 BAD REQUEST"
        assert result_data == "email"

        data = {
            "username": "newTestUser",
            "email": "exampletest.com",
            "password": "Just&1Test"
        }

        result = client.post(url_for('miscapi.registration_action'), json = data)
        result_data = result.get_json()
        assert result_data != None
        assert result.status == "400 BAD REQUEST"
        assert result_data == "email"

        data = {
            "username": "newTestUser",
            "email": "example@4test.com",
            "password": "Just"
        }

        result = client.post(url_for('miscapi.registration_action'), json = data)
        result_data = result.get_json()
        assert result_data != None
        assert result.status == "400 BAD REQUEST"
        assert result_data == "password"

        data = {
            "username": "lk",
            "email": "example@est.com",
            "password": "Just&1Test"
        }

        result = client.post(url_for('miscapi.registration_action'), json = data)
        result_data = result.get_json()
        assert result_data != None
        assert result.status == "400 BAD REQUEST"
        assert result_data == "username"

    def test_stats(self, session, client):
        """
        Tests stats in miscapi.py
        """
        #create valid token
        user_id = self.user_list[0]
        token = str(user_id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=token).count() != 0) :
            token = str(user_id).zfill(10) + str(uuid.uuid4())

        token = UserToken(user_id=user_id,token=token)
        token.update = datetime.utcnow()
        token.created = datetime.utcnow()
        session.add(token)
        session.commit()

        result = client.get(url_for('miscapi.stats') + '?token=' + token.token)
        result_data = result.get_json()
        assert result_data is not None
        assert 'user_count' in result_data
        assert 'module_count' in result_data
        assert 'project_count' in result_data
        assert 'package_count' in result_data

        result = client.get(url_for('miscapi.stats') + '?token=bladfjoagsag')
        result_data = result.get_json()
        assert result_data is not None
        assert result.status == "403 FORBIDDEN"
        assert result_data == "Invalid token."

        result = client.get(url_for('miscapi.stats'))
        result_data = result.get_json()
        assert result_data is not None
        assert result.status == "403 FORBIDDEN"
        assert result_data == "Invalid token."
