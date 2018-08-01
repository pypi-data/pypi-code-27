import re

def extract(text):
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    print(email)
