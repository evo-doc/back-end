
from evodoc.entity import User, UserType, UserToken, db

def initUserSeeds():
    """
    Run all user seeds
    """
    __baseUserType()
    __userInsert()

def __userInsert():
    userList = []
    userAdmin = User("Admin", "admin@nimda.exp", "SuperSecret", None, None, True)
    userAdmin.user_type_id = UserType.get_type_by_name('ADMIN').id
    userAdmin.activated = True
    userList.append(userAdmin)

    userEntities = User.query.all()

    for user in userEntities:
        for seedUser in userList:
            if (user.name == seedUser.name):
                userList.remove(seedUser)

    for seedUser in userList:
        db.session.add(seedUser)
        db.session.commit()
        print("Inserting: ")
        print(seedUser.name)

def __baseUserType():
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
        db.session.add(user_type)
        db.session.commit()