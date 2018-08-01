import sqlalchemy
from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.expression import and_
import sqlite3

engine = create_engine('sqlite:///db/users.db', connect_args={'check_same_thread':False}, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

association_table = Table('contacts', Base.metadata,
                          Column('owner_id', Integer, ForeignKey('users.id')),
                          Column('contact_id', Integer, ForeignKey('users.id'))
                          )

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return '<User(username={}'.format(self.username)

Base.metadata.create_all(engine)


def username_is_used(username):
    """

    :return: Boolean
    """
    is_used = False

    for _ in session.query(User.username). \
            filter(User.username == username):
        is_used = True
        break
    return is_used

def check_login_password(username, password):
    """

    :return: Boolean
    """
    for _ in session.query(User.username). \
            filter(User.username == username, User.password == password):
        return True
    return False

def add_user(username, password):
    """

    :return:
    """
    session.add(User(username=username, password=password))
    session.commit()


def find_id(username):
    """

    :param username:
    :return: int id of the user with such username
    """
    for user in session.query(User).filter(User.username == username):
        return user.id


def contact_user_is_present(contact):
    """

    :param username:
    :return: int id of the user with such username
    """
    present = False
    result = engine.execute("SELECT users.id from users WHERE users.id == (?)", contact)
    if len([row['id'] for row in result]) != 0:
        present = True
    return present

def contact_is_present(owner, contact):
    """

    :param username:
    :return: int id of the user with such username
    """
    present = False
    result = engine.execute("SELECT contacts.owner_id, contacts.contact_id from contacts WHERE owner_id == (?) AND contact_id == (?)", owner, contact)
    if len([row['owner_id'] for row in result]) != 0:
        present = True
    return present

def list_contacts(owner):
    """

    :param owner: name of the owner
    :return: list of names of contacts
    """
    owner = find_id(owner)
    username_ids = engine.execute("SELECT contacts.owner_id, contacts.contact_id from contacts WHERE owner_id == (?)", owner)
    usernames = []
    ids = [row['contact_id'] for row in username_ids]
    for id in ids:
        result = engine.execute("SELECT users.username FROM users WHERE users.id == (?)", id)
        name = [row['username'] for row in result]
        usernames.extend(name)
    return usernames

def list_usernames():
    """

    :param username:
    :return: int id of the user with such username
    """
    usernames = engine.execute("SELECT users.username FROM users")
    return [row[0] for row in usernames]

def add_contact(owner, contact):
    """

    :param owner: int owner id in users table
    :param contact: int the person that the owner wants to add as a contact
    :return: None
    """
    with engine.begin() as connection:
        connection.execute("INSERT INTO contacts (owner_id, contact_id) VALUES (?, ?)", owner, contact)

def delete_contact(owner, contact):
    """

    :param owner: int owner id in users table
    :param contact: int the person that the owner wants to delete as a contact
    :return: None
    """

    with engine.begin() as connection:
        connection.execute("DELETE FROM contacts WHERE owner_id == (?) AND contact_id == (?)", owner, contact)

if __name__ == "__main__":
    print(list_usernames())
