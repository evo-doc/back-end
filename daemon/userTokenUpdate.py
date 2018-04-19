#needs to load connection from default file
#needs import UserToken
#run every xxx 

from sqlalchemy.engine import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
db = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()

session.query(UserToken).filter(UserToken.created +  timedelta(hours=24) < datetime.utcnow()).delete()

session.query(UserToken).filter(UserToken.update +  timedelta(hours=2) < datetime.utcnow()).delete()

session.commit()

