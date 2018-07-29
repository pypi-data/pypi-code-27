import requests
import json
import sys

username = sys.argv[1]

def main(uname = username):
    url = 'https://gitlab.com/api/v4/users?username=' + uname
    firstresponse = requests.get(url, verify = True)

    firstdata = firstresponse.json()
    firstid = firstdata[0]['id']

    endpoint = 'https://gitlab.com/api/v4/users/' + str(firstid)
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    data = response.json()

    username = data['username']
    bio = data['bio']
    location = data['location']
    twitter = data['twitter']
    linkedin = data['linkedin']
    skype = data['skype']
    website_url = data['website_url']
    uid = data['id']
    state = data['state']
    avatar_url = data['avatar_url']
    web_url = data['web_url']
    print('Username : ', username)

    if bio != None:
        print('Bio      : ', bio)

    if location != None:
        print('Location : ', location)

    if twitter != "":
        print('Twitter  :  https://twitter.com/' + twitter)

    if linkedin != "":
        print('Linkedin :  https://linkedin.com/in/' + linkedin)

    if skype != "":
        print('Skype    : ', skype)

    if website_url != "":
        print('Website  : ', website_url)

    print('ID       : ', uid)
    print('State    : ', state)
    print('Avatar   : ', avatar_url)
    print('Link     : ', web_url)
