from evodoc.entity.user import User, UserType, UserToken
from evodoc.app import db

def userInsert():
    userList = []
    userList.append(User("Admin", "admin@nimda.exp", "SuperSecret", None, None, True))

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

