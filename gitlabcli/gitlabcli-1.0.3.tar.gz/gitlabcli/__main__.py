from gitlabcli import main, Fore, Style
from colorama import init
import sys
init()

try:
    uname = sys.argv[1]
    main(uname)
except:
    print (Fore.YELLOW + 'Usage: gitlab <username> '+ Style.RESET_ALL + Fore.GREEN + '\nExample: gitlab yoginth')
