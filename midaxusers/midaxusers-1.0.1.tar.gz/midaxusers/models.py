from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, String, Integer, DateTime, Column, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func, expression
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.types import PickleType
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import abort
from sqlalchemy import types, and_, or_
from sqlalchemy.dialects.mysql.base import MSBinary
#from sqlalchemy.schema import Column
import uuid

db = SQLAlchemy()
migrate = Migrate()

def HybridUniqueIdentifier():
    return String().with_variant(UNIQUEIDENTIFIER, 'mssql').with_variant(RAW(16), 'oracle')


def generate_uuid():
   return str(uuid.uuid4())

class User(db.Model):
    id = Column(Integer, primary_key=True)
    uuid = Column(HybridUniqueIdentifier(), unique=True, index = True, default=generate_uuid)
    domain = Column(String(64), index=True)
    username = Column(String(64), index=True)
    email = Column(String(120), index=True, unique=True)
    role = Column(Integer)
    password_hash = Column(String(256))
    force_password_change = Column(Boolean, server_default=expression.false())
    active = Column(Boolean, server_default=expression.true())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('domain', 'username', name='domain_user_uq'),
                     )

    def __init__(self, identifier = None, uuid = None, username = None, domain = None):

        if identifier is not None:
            identifier = identifier.casefold()

        if username is not None:
            username = username.casefold()

        if domain is not None:
            domain = domain.casefold()
            
        if uuid is not None:
            self.uuid = uuid

        if username is not None and domain is not None:
            if '^' in username or '@' in username:
                raise ValueError('Username cannot contain ^ or @')
            self.username = username
            self.domain = domain
        
        if identifier is not None:
            if '@' in identifier:
                self.email = identifier
            else:
                split_path = identifier.split('^')
                self.username = split_path[-1]
                self.domain = '^'.join(split_path[:-1])

    def serialize(self):
        return {            
            'uuid': self.uuid,
            'domain': self.domain,
            'username': self.username,
            'email':self.email,
            'role':self.role
        }

    def password_set(self, value):
        old_hash = self.password_hash
        try:
            self.password_hash = generate_password_hash(value, method='pbkdf2:sha512', salt_length=16)
        except:
            self.password_hash = old_hash
            raise ValueError("Cannot generate hash")
    
    def search(self):        
        q = self.query
        if self.username is not None:
            q = q.filter_by(username = self.username)
        if self.domain is not None:
            q = q.filter_by(domain = self.domain)
        if self.email is not None:
            q = q.filter_by(email = self.email)
        if self.uuid is not None:
            q = q.filter_by(uuid = self.uuid)

        q=q.filter_by(active = True)

        return q.first()

    def search_inactive(self):        
        q = self.query
        if self.username is not None:
            q = q.filter_by(username = self.username)
        if self.domain is not None:
            q = q.filter_by(domain = self.domain)
        if self.email is not None:
            q = q.filter_by(email = self.email)
        if self.uuid is not None:
            q = q.filter_by(uuid = self.uuid)

        q=q.filter_by(active = False)

        return q.first()
        

    password = property()
    password = password.setter(password_set)    

    def check_password(self, value):        
        if self.password_hash is not None and value is not None:
            return check_password_hash(self.password_hash, value)
        return False

    def __repr__(self):
        return '<Domain {} User {}>'.format(self.domain, self.username)
    
    def __str__(self):
          return '<{}@{}>'.format(self.username, self.domain)  

class UserAttributes(db.Model):
    user_uuid = Column(HybridUniqueIdentifier())
    name = Column(String(64))
    value = Column(String(64))
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (PrimaryKeyConstraint('user_uuid', 'name', name='userattributes_pk'),
                     )

    def serialize(self):
        return self.name, self.value
                
    def __repr__(self):
        return '<{}:{}>'.format(self.name, self.value)  


def verify_domain_rights(loggeduser, targetuser = None, targetdomain = None):
    if targetdomain is None:   
        if targetuser is None:
           abort(404)

        if targetuser.domain is None:
            targetuser = targetuser.search() 

        if targetuser is None:
            abort(404)

        targetdomain = targetuser.domain

    targetdomain = targetdomain.casefold()

    userdomainlevels = loggeduser.domain.split('^')
    targetdomainlevels  = targetdomain.split('^')
    zipped_tuples = zip(userdomainlevels, targetdomainlevels)
    for user_element, target_element in zipped_tuples:
        if user_element != target_element:
            return False
            
    if len(userdomainlevels) > len(targetdomainlevels):
        return False

    return True

def verify_unique_user_in_domain(newuser):   
    domainlevels = newuser.domain.split('^')
    current_domain_depth = ''
    query = db.session.query(User)  
    
    ors = [] 
    current_domain_depth = domainlevels[0]
    ors.append( 
             User.domain == current_domain_depth
        )
        
    for domainlevel in domainlevels[1:]: 
        current_domain_depth += '^{}'.format(domainlevel)
        ors.append( 
             User.domain == current_domain_depth
        )

    query = query.filter(and_(
        or_(*ors),
        User.username == newuser.username
        )
        )     

    user = query.first()

    if user is not None:
        return False

    return True

def verify_unique_email(email_to_check):   
    user = User.query.filter_by(email = email_to_check).first()

    if user is not None:
        return False

    return True