# -*- coding: utf-8 -*-

#   Copyright 2018 Jim Martens
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""calendarsync.calendarsync: provides entry point main()"""
import argparse
import datetime
import glob
import os
from os.path import isdir

import pkg_resources
from ics import Calendar
from urllib.request import urlopen
from urllib.parse import urlparse, ParseResult


def main() -> None:
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        description="Synchronizes jekyll event collection with remote calendar",
    )
    parser.add_argument('calendar_url', type=validate_url, help='URL to the remote calendar ICS location')
    parser.add_argument('event_collection_path', type=validate_dir, help='Path to event collection directory')
    args = parser.parse_args()
    
    sync(args.calendar_url, args.event_collection_path)


def sync(calendar_url: str, event_collection_path: str) -> None:
    """
    Synchronizes the event collection with a remote calendar.
    
    :param calendar_url: URL to remote calendar ICS
    :param event_collection_path: path to event collection directory
    """
    calendar = Calendar(urlopen(calendar_url).read().decode('utf-8'))
    template_filename = pkg_resources.resource_filename(
        __package__,
        'event_template.markdown'
    )
    with open(template_filename, 'r', encoding='utf-8') as template:
        template_content = template.read()
    
    # remove previous event files in directory to allow the removal of events in calendar
    files = glob.glob(event_collection_path + '*.markdown')
    for file in files:
        os.remove(file)
    
    for event in calendar.events:
        event_content = template_content.replace('<name>', event.name)
        created: datetime.datetime = event.created
        created_str = created.isoformat(sep=' ')
        event_content = event_content.replace('<date>', created_str)
        begin: datetime.datetime = event.begin
        begin_str = begin.isoformat(sep=' ')
        event_content = event_content.replace('<begin>', begin_str)
        end: datetime.datetime = event.end
        end_str = end.isoformat(sep=' ')
        event_content = event_content.replace('<end>', end_str)
        event_content = event_content.replace('<location>', event.location)
    
        event_filename = begin.date().isoformat() + '-' + event.name.replace(' ', '_') + '.markdown'
        with open(event_collection_path + event_filename, 'w', encoding='utf-8', newline='\n') as event_file:
            event_file.write(event_content)


def validate_url(url: str) -> str:
    """
    Validates a URL and returns it on success.
    
    :param url: URL to verify
    :return: verified URL
    :raises: argparse.ArgumentTypeError if URL is invalid
    """
    parsed_url: ParseResult = urlparse(url)
    if parsed_url.netloc == '' or parsed_url.scheme == '':
        raise argparse.ArgumentTypeError(f"'{url}' is not a valid URL.")
    
    return url


def validate_dir(directory: str) -> str:
    """
    Validates a directory path and returns it on success.
    
    :param directory: path to directory to verify
    :return: verified directory path
    :raises: argparse.ArgumentTypeError if directory does not exist
    """
    if not isdir(directory):
        raise argparse.ArgumentTypeError(f"'{directory}' is not an existing directory.")
    return directory
