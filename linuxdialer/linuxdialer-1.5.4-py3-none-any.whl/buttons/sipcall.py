"""
Module for VoIP call Implementation.
"""
import subprocess
from pathlib import Path

from phonenumbers import format_number, PhoneNumberFormat

name = "VoIP call"
icon = Path(__file__).parent / 'icons' / 'call.png'
apps_required = ('ekiga',)


def launch(parent, phonenumber_obj):
    """
    Open VoIP client (Ekiga) to call
    :param parent: reference of main pop-up window
    :param phonenumber_obj: Phonenumber class object
    :return: None
    """
    phonenumber = format_number(phonenumber_obj, PhoneNumberFormat.E164)  # phonenumber in E164 format
    subprocess.call(['ekiga', '-c', phonenumber])
