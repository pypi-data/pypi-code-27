import re
def check(id):

     email = re.match('[^@]+@[^@]+\.[^@]+', id)

     if email:
         print("True")
     else:
         print("False")