import pytest, json, uuid
from datetime import datetime, timedelta
from evodoc import DbException, ApiException, login, authenticate, check_token_exists
from evodoc.entity import User, UserType, UserToken

@pytest.mark.usefixture("session")
class TestLogin:
    user_list = []
    token_list = []

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
            session.add(user_type)
            session.commit()

        user = User("Admin", "admin@nimda.exp", "SuperSecret", None, None, True)
        user.user_type_id = UserType.get_type_by_name('ADMIN').id
        user.activated = True
        session.add(user)
        session.commit()
        self.user_list.append(user)
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

    def test_login(self, session):
        """
        Perform login test
        """
        username = ""
        password = ""
        with pytest.raises(ApiException) as err:
            login(username, password)
        assert str(err.value) == "(400, 'userpass')"

        username = "NotAnUser"
        with pytest.raises(ApiException) as err:
            login(username, password)
        assert str(err.value) == "(400, 'userpass')"

        username = "Admin"
        with pytest.raises(ApiException) as err:
            login(username, password)
        assert str(err.value) == "(400, 'userpass')"

        password = "SuperSecret"
        result = login(username, password)

        token_from_db = session.query(UserToken).filter_by(user_id = self.user_list[0].id).first()
        assert token_from_db.token == result.token

        username = "Test"
        with pytest.raises(ApiException) as err:
            login(username, password)

        test_user = next((x for x in self.user_list if x.name == "Test"), None)
        assert test_user is not None, "User for this test was not found in Db, something is wrong :/"
        token_from_db = session.query(UserToken).filter_by(user_id = test_user.id).first()
        result_obj = err.value.message
        assert result_obj['verified'] == "false" and result_obj['token'] == token_from_db.token

    def test_authenticate(self, session):
        """
        Authenticate test
        """
        result = authenticate()
        assert result == None

        user = next((x for x in self.user_list if x.name == "Test"), None)

        old_token = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=old_token).count() != 0) :
            old_token = str(user.id).zfill(10) + str(uuid.uuid4())

        old_token = UserToken(user_id=user.id,token=old_token)
        old_token.update = datetime.utcnow() - timedelta(hours=4)
        old_token.created = datetime.utcnow() - timedelta(hours=48)
        session.add(old_token)
        session.commit()

        result = authenticate(old_token.token)
        assert result == None

        result = authenticate(None, True, old_token.user_id)
        assert result != None
        assert result != old_token.token
        token_from_db = session.query(UserToken).filter_by(user_id = user.id).order_by(UserToken.id.desc()).first()
        assert result.token == token_from_db.token

    def test_check_token_exists(self, session):
        """
        Test for check_token_exists
        """
        token = None
        result = check_token_exists(token)
        assert result == None

        token = "fkdjasghgopgasdf"
        result = check_token_exists(token)
        assert result == None

        user = next((x for x in self.user_list if x.name == "Test"), None)
        old_token = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=old_token).count() != 0) :
            old_token = str(user.id).zfill(10) + str(uuid.uuid4())

        old_token = UserToken(user_id=user.id,token=old_token)
        old_token.update = datetime.utcnow() - timedelta(hours=4)
        old_token.created = datetime.utcnow() - timedelta(hours=48)
        session.add(old_token)
        session.commit()

        result = check_token_exists(token)
        assert result == None

        result = check_token_exists(old_token.token)
        assert result == old_token
