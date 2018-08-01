# keys

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
CONTACT_NAME = 'contact_name'
RESPONSE = 'response'
ERROR = 'error'
CONTACTS = 'contacts'
ADD = 'add'
DEL = 'del'
ADDR = 'addr'
CHECK = 'check'
IMAGE = 'image'
CONTACT_IMAGE = 'contact_image'
# values

PRESENCE = 'presence'
MSG = 'msg'
TO = 'to'
FROM = 'from'
MESSAGE = 'message'
CONTACT = 'contact'
ADD_CONTACT = 'add_contact'
ADD_USER = 'add_user'
DEL_CONTACT = 'del_contact'
LIST_CONTACTS = 'list_contacts'
PASSWORD = 'password'

# responses codes

BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400
SERVER_ERROR = 500
USERNAME_ALREADY_USED = 600

# codes tuple

RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR, USERNAME_ALREADY_USED)
