import requests
import json
import sys
from colorama import Fore, init
init()

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
    print('Username : ' + Fore.GREEN + username)
    print(Style.RESET_ALL)

    if bio != None:
        print('Bio      : ' + Fore.GREEN + bio)
        print(Style.RESET_ALL)

    if location != None:
        print('Location : ' + Fore.RED + location, end = '')
        print(Style.RESET_ALL)

    if twitter != "":
        print('Twitter  : ' + Fore.BLUE + 'https://twitter.com/' + twitter, end = '')
        print(Style.RESET_ALL)

    if linkedin != "":
        print('Linkedin : ' + Fore.BLUE + 'https://linkedin.com/in/' + linkedin, end = '')
        print(Style.RESET_ALL)

    if skype != "":
        print('Skype    : ' + Fore.YELLOW + skype, end = '')
        print(Style.RESET_ALL)

    if website_url != "":
        print('Website  : ' + Fore.BLUE + website_url, end = '')
        print(Style.RESET_ALL)

    print('ID       : ' + Fore.MAGENTA + str(uid), end = '')
    print(Style.RESET_ALL)
    print('State    : ' + Fore.MAGENTA + state, end = '')
    print(Style.RESET_ALL)
    print('Avatar   : ' + Fore.BLUE + avatar_url, end = '')
    print(Style.RESET_ALL)
    print('Link     : ' + Fore.BLUE + web_url, end = '')
    print(Style.RESET_ALL)

main(username)