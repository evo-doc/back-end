#needs to load connection from default file

from sqlalchemy.engine import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta	
db = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)


Base.metadata.create_all(db)
#ed_user = User(id=0,name='ed', fullname='Ed Jones', password='edspassword')
#session.add(ed_user)

for i in range (1, 10):
	session.add(User(name='kek', fullname='Kektimus Prime', password='password', date=datetime.utcnow()  - timedelta(hours=9)))

#session.commit()

#for i in session.query(User).filter_by(name='kek'):
#	i.delete()
#	print (i.id, "  ", i.name)

session.query(User).filter(User.date +  timedelta(hours=9) < datetime.utcnow()).delete()

session.commit()

kek="kek"

while session.query(User).filter_by(	name=kek).count() > 100:
	print(kek)
	break
