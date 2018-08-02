import requests
import gitlab
import json
import sys
from colorama import Fore, Style, init
init()

def main(uname):
    data = gitlab.get(uname)

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
