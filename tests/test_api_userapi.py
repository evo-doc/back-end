import pytest, uuid
from datetime import datetime, timedelta
from flask import url_for
from evodoc.entity import User, UserToken, UserType

@pytest.mark.usefixture("session")
class TestUserapi:
    user_list = []
    token_list = []
    user_type_list = []

    @pytest.fixture(scope="class", autouse = True)
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
        session.commit()
        ttoken = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=ttoken).count() != 0) :
            ttoken = str(user.id).zfill(10) + str(uuid.uuid4())

        ttoken = UserToken(user_id=user.id,token=ttoken)
        ttoken.update = datetime.utcnow()
        ttoken.created = datetime.utcnow()
        session.add(ttoken)
        session.commit()
        self.token_list.append(ttoken.token)
        self.user_list.append(user.id)
        user = User("Test", "te@te.exp", "SuperSecret", None, None, True)
        session.add(user)
        session.commit()
        ttoken = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=ttoken).count() != 0) :
            ttoken = str(user.id).zfill(10) + str(uuid.uuid4())

        ttoken = UserToken(user_id=user.id,token=ttoken)
        ttoken.update = datetime.utcnow()
        ttoken.created = datetime.utcnow()
        session.add(ttoken)
        session.commit()
        self.token_list.append(ttoken.token)
        self.user_list.append(user.id)

        yield
        session.query(User).delete()
        session.query(UserType).delete()
        session.query(UserToken).delete()
        session.commit()

    def test_get_user_by_id_action(self, session, client):
        """
        Test for GET method for user
        """
        token = self.token_list[0]
        result = client.get(url_for('user.get_user_by_id_action') + "?token=" + token)
        result_data = result.get_json()
        assert result is not None
        assert result.status == "404 NOT FOUND"
        assert result_data == "User not found."

        result = client.get(url_for('user.get_user_by_id_action') + "?token=" + token + "&user_id=" + str(self.user_list[0]))
        result_data = result.get_json()
        assert result is not None
        assert 'name' in result_data
        assert 'email' in result_data
        assert 'id' in result_data
        assert result_data['id'] == self.user_list[0]

        result = client.get(url_for('user.get_user_by_id_action') + "?user_id=" + str(self.user_list[0]))
        result_data = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_data == "Invalid token."

    def test_delete_user(self, session, client):
        """
        Test delete user
        """
        token = self.token_list[0]
        user_id = self.user_list[1]

        result = client.delete(url_for('user.delete_user'))
        result_json = result.get_json()
        assert result_json is not None
        assert result.status == "400 BAD REQUEST"
        assert result_json == "data"

        data = {
            'token': 'InvalidToken',
            'user_id': user_id
        }
        result = client.delete(url_for('user.delete_user'), json = data)
        result_json = result.get_json()
        assert result_json is not None
        assert result.status == "403 FORBIDDEN"
        assert result_json == "Invalid token."
        user_from_db = User.query.filter_by(id = user_id).first()
        assert user_from_db.active == True

        data = {
            'token': token,
            'user_id': user_id
        }
        result = client.delete(url_for('user.delete_user'), json = data)
        result_json = result.get_json()
        assert result_json is not None
        assert result.status == "200 OK"
        assert "data" in result_json
        user_from_db = User.query.filter_by(id = user_id).first()
        assert user_from_db.active == False

        #cleanup
        user_from_db.active = True
        session.commit()

    def test_update_user(self, session, client):
        """
        Test update method
        """
        url = url_for('user.update_user')
        token = self.token_list[0]
        user_id = self.user_list[0]

        data = {
            'token': token,
            'user_id': user_id,
            'name': 'NoAdminForYa_hacked'
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "200 OK"
        assert result_json['name'] == 'NoAdminForYa_hacked'
        assert result_json['id'] == user_id
        #reload user from db
        user = self.user_list[0] = User.query.filter_by(id = user_id).first()
        assert result_json['name'] == user.name

        data = {
            'token': token,
            'user_id': 0,
            'name': 'NoAdminForYa_hacked'
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "404 NOT FOUND"
        assert result_json == "User not found."

        data = {
            'token': "InvalidToken",
            'user_id': user_id,
            'name': 'NoAdminForYa_hacked'
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_json == "Invalid token."

    def test_get_user_all_action(self, session, client):
        """Test get user list"""
        token = self.token_list[0]
        url = url_for('user.get_user_all_action')

        user_list = []
        for user in User.query.all():
            user_list.append(user.serialize())

        result = client.get(url + "?token=" + token)
        result_json = result.get_json()
        assert result.status == "200 OK"
        assert result_json == user_list

        result = client.get(url + "?token=InvalidToken")
        result_json = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_json == "Invalid token."

    def test_activation_action(self, session, client):
        """
        Test users activation
        """
        token = self.token_list[1]
        user_id = self.user_list[1]
        url = url_for('user.activation_action')

        data = {
            'token': token
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "200 OK"
        assert "data" in result_json
        assert result_json["data"] == "activated"
        user = User.query.filter_by(id = user_id).first()
        assert user.activated == True

        user.activated = False
        session.commit()

        #already activated
        token = self.token_list[0]
        user_id = self.user_list[0]
        url = url_for('user.activation_action')

        data = {
            'token': token
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "400 BAD REQUEST"
        assert result_json == "User has been already activated."

        data['token'] = 'InvalidToken'

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_json == "Invalid token."

    def test_is_user_authorised(self, session, client):
        """
        Test user authorised method
        """
        token = "InvalidToken"
        url = url_for('user.is_user_authorised')

        data = {
            'token': token
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_json == "Invalid token."

        token = self.token_list[1]

        data = {
            'token': token
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "200 OK"
        assert 'verified' in result_json
        assert result_json['verified'] == "false"

        user_id = self.user_list[0].id

        ttoken = str(user_id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=ttoken).count() != 0) :
            ttoken = str(user_id).zfill(10) + str(uuid.uuid4())

        ttoken = UserToken(user_id=user_id,token=ttoken)
        ttoken.update = datetime.utcnow() - timedelta(hours=4)
        ttoken.created = datetime.utcnow() - timedelta(hours=48)
        session.add(ttoken)
        self.token_list.append(ttoken)
        session.commit()

        data['token'] = ttoken.token

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "403 FORBIDDEN"
        assert result_json == "Invalid token."

        token = self.token_list[0]

        data = {
            'token': token
        }

        result = client.post(url, json = data)
        result_json = result.get_json()
        assert result.status == "200 OK"
        assert 'verified' in result_json
        assert result_json['verified'] == "true"