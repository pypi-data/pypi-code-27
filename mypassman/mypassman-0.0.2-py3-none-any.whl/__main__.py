#!/usr/bin/env python3

from .passman import initialize

def main():
    initialize()
    check_users()
    login()
    menu_loop()

main()