import hashlib

def get(email, size = 250):
	result = hashlib.md5(email.encode())
	print('https://secure.gravatar.com/avatar/' + result.hexdigest() + '?s=' + str(size))