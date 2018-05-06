import pytest, uuid
from datetime import datetime, timedelta
from evodoc import DbException, ApiException, authenticate
from evodoc.api import validate_token, validate_data
from evodoc.entity import User, UserType, UserToken

@pytest.mark.usefixture("session")
class TestApi:
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
        ttoken = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=ttoken).count() != 0) :
            ttoken = str(user.id).zfill(10) + str(uuid.uuid4())

        ttoken = UserToken(user_id=user.id,token=ttoken)
        ttoken.update = datetime.utcnow() - timedelta(hours=4)
        ttoken.created = datetime.utcnow() - timedelta(hours=48)
        session.add(ttoken)
        self.token_list.append(ttoken)
        self.user_list.append(user)
        session.commit()

        user = User("Test", "te@te.exp", "SuperSecret", None, None, True)
        session.add(user)
        self.user_list.append(user)

        ttoken = str(user.id).zfill(10) + str(uuid.uuid4())
        #Check if token is unique
        while (UserToken.query.filter_by(token=ttoken).count() != 0) :
            ttoken = str(user.id).zfill(10) + str(uuid.uuid4())

        ttoken = UserToken(user_id=user.id,token=ttoken)
        ttoken.update = datetime.utcnow()
        ttoken.created = datetime.utcnow()
        session.add(ttoken)
        self.token_list.append(ttoken)
        session.commit()

        yield
        session.query(User).delete()
        session.query(UserType).delete()
        session.query(UserToken).delete()
        session.commit()
        self.user_list = []
        self.token_list = []

    def test_validate_token(self, session):
        """
        Test validate_token
        """
        token = "OFNdaosofjnoasdjngonabgo"
        with pytest.raises(ApiException) as err:
            result = validate_token(None)
        assert err.value.message == "Invalid token."

        token = "OFNdaosofjnoasdjngonabgo"
        with pytest.raises(ApiException) as err:
            result = validate_token(token)
        assert err.value.message == "Invalid token."

        token = self.token_list[0].token
        with pytest.raises(ApiException) as err:
            result = validate_token(token)
        assert err.value.message == "Invalid token."

        token = self.token_list[1].token
        with pytest.raises(ApiException) as err:
            result = validate_token(token)
        assert err.value.message["token"] != token
        token = UserToken.query.filter_by(user_id = self.token_list[1].user_id).order_by(UserToken.id.desc()).first()
        assert err.value.message["token"] == token.token

        self.user_list[1].activated = True
        session.commit()

        result = validate_token(token.token)
        assert result != None
        assert result == token.token


    def test_validate_data(self):
        """
        Test validate_data
        """
        with pytest.raises(ApiException) as err:
            validate_data({})
        assert err.value.message == "data"
        assert err.value.errorCode == 400

        validate_data({"test": "noerror"})

        with pytest.raises(ApiException) as err:
            validate_data({"test": "noerror"}, ["user_id"])
        assert err.value.message == "data"
        assert err.value.errorCode == 400

        validate_data({"test": "noerror"}, ["test"])
