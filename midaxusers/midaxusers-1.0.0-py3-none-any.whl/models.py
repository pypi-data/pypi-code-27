from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import types, and_, or_
from sqlalchemy.dialects.mysql.base import MSBinary
from sqlalchemy.schema import Column
import uuid

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UNIQUEIDENTIFIER, unique=True, index = True, default=uuid.uuid4())
    domain = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.Integer)
    password_hash = db.Column(db.String(256))

    __table_args__ = (UniqueConstraint('domain', 'username', name='domain_user_uq'),
                     )

    def __init__(self, identifier = None, uuid = None):
        if uuid is not None:
            self.uuid = uuid
        else:
            if '@' in identifier:
                self.email = identifier
            else:
                split_path = identifier.split('.')
                self.username = split_path[-1]
                self.domain = '.'.join(split_path[:-1])

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
            q = q.filter_by(uuin = self.uuid)

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
    user_uuid = db.Column(UNIQUEIDENTIFIER)
    name = db.Column(db.String(64))
    value = db.Column(db.String(64))

    __table_args__ = (PrimaryKeyConstraint('user_uuid', 'name', name='userattributes_pk'),
                     )

    def serialize(self):
        return self.name, self.value
                
    def __repr__(self):
        return '<{}:{}>'.format(self.name, self.value)  


def verify_domain_rights(loggeduser, targetdomain):    
    userdomainlevels = loggeduser.domain.split('.')
    targetdomainlevels  = targetdomain.split('.')
    zipped_tuples = zip(userdomainlevels, targetdomainlevels)
    for user_element, target_element in zipped_tuples:
        if user_element != target_element:
            return False
            
    if len(userdomainlevels) > len(targetdomainlevels):
        return False

    return True

def verify_unique_user_in_domain(newuser):   
    domainlevels = newuser.domain.split('.')
    current_domain_depth = ''
    query = db.session.query(User)  
    
    ors = [] 
    current_domain_depth = domainlevels[0]
    ors.append( 
             User.domain == current_domain_depth
        )
        
    for domainlevel in domainlevels[1:]: 
        current_domain_depth += '.{}'.format(domainlevel)
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