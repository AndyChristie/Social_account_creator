from sqlalchemy import create_engine, Column, Integer, \
     String, Boolean, PickleType
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

#basedir = os.path.abspath(os.path.dirname(__file__))

engine  = create_engine('sqlite:///:database1', echo=True)
Base    = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#-----------------------------------------------------------------------

class Basetable():
    first_name       = Column(String(64))
    last_name        = Column(String(64))
    id               = Column(Integer, primary_key=True)
    email            = Column(String(64), unique=True)
    password         = Column(String(64))
    cookies          = Column(PickleType, unique=True)
    cookies_filtered = Column(Boolean)# filter out the cookies that aren't the same domain as the site
    word_list_count  = Column(Integer)

#-----------------------------------------------------------------------

class Accounts(Base):
    __tablename__ = 'Accounts'

    site      = Column(Integer, primary_key=True)
    email     = Column(String(64), unique=True)
    accounts  = Column(Integer)
    followers = Column(Integer)

    def __repr__(self):
        return "<Accounts(site='%s', accounts='%s', followers='%s')>"%(
                                self.site, self.accounts, self.followers)

#-----------------------------------------------------------------------

class Gmail(Base, Basetable):
    __tablename__ = 'Gmail'

#-----------------------------------------------------------------------

class Twitter(Base, Basetable):
    __tablename__ = 'Twitter'
    #2 years expiration
    limit_reached = Column(Boolean)

#-----------------------------------------------------------------------

class Tumblr(Base, Basetable):
    __tablename__ = 'Tumblr'

#-----------------------------------------------------------------------

class Reddit(Base, Basetable):
    __tablename__ = 'Reddit'

#-----------------------------------------------------------------------

class Digg(Base, Basetable):
    __tablename__ = 'Digg'

#-----------------------------------------------------------------------

class Pinterest(Base, Basetable):
    __tablename__ = 'Pinterest'

#-----------------------------------------------------------------------

class Instagram(Base, Basetable):
    __tablename__ = 'Instagram'

#-----------------------------------------------------------------------

class Linkedin(Base, Basetable):
    __tablename__ = 'Linkedin'

'''
class Livejournal(Base, Basetable):
    __tablename__ = 'Livejournal'

class Stumbleupon(Base, Basetable):
    __tablename__ = 'Stumble_upon'
'''


# Have captcha services

Base.metadata.create_all(engine)



'''
twitt = Twitter('1', 'andy.christie93@hotmail.co.uk', 'Andy_is_cool')
session.add(twitt)
session.commit()
'''
'''

twit = Twitter(id=3, email='andychristie93@hotmail.co.uk', password='Andy_is_cool') #####--++++++--#####
session.add(twit) #####--++++++--#####
session.commit() #####--++++++--#####

'''
