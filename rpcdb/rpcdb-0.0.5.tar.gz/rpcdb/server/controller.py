#! usr/bin/python3

from sqlconnection import Connection
from functools import wraps
from mysql.connector import Error

def use_local(**config):
    return Connection.connect(**config)
    
def error_decor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__
        
        try:
            results = func(*args, **kwargs)
        except Error as e:
            if e.errno == 1062:
                return "This record already exists in the database"
            else:
                return False, str(e)
        else:
            if name == 'delete':
                return "Deleted record successfully"
                
            elif name == 'save':
                return "Saved record successfully"
                
            elif name == 'update':
                return "Updated record successfully"
            else:
                return results
 
    return wrapper

def description(sql):
    with Connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql)
            return [result[0] for result in cur.fetchall()]
        except:
            return []   
          
@error_decor  
def execute_many(sql, data):
    with Connection() as conn:
        cur = conn.cursor()
        return cur.executemany(sql, data) 
        
@error_decor  
def execute(sql):
    with Connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:      
            return str(e)
        else:
            if 'select' in sql.lower():
                return cur.fetchall()
            else:
                return True
    
    
def get(sql, as_dict, only_one):
    with Connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            if as_dict:    
                return [str(e), {}]
            else:
                return [str(e), []]
        else:
            colnames = [d[0] for d in cur.description]
            if not only_one:
                if as_dict:
                    return [dict(zip(colnames, r)) for r in cur.fetchall()]
                return cur.fetchall()
                    
            results = cur.fetchone()
            if as_dict:
                return {col: val for col, val in zip(colnames, results)} if results else {}
            return results
             
         
@error_decor      
def save(sql):
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(sql)
            
@error_decor        
def update(sql):
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(sql)


@error_decor    
def delete(sql):
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(sql)

remote_calls = [save, update, delete, execute, execute_many, get, description]


