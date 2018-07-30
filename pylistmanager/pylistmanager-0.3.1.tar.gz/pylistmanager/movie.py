# pylistmanager
# Copyright (C) 2018  Sotiris Papatheodorou
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-


import csv
import datetime
import os
import sys
from colorama import Fore, Back, Style
from .listitem import *


# Global variables
movie_attributes = ['name', 'year', 'rating', 'max_rating', 'tags', 
                    'date_watched', 'imdb_URI', 'rtomatoes_URI',
                    'letterboxd_URI', 'date_added']
csv_header_columns = ['Name', 'Year Released', 'Rating', 'Max Rating', 'Tags',
                      'Date Watched', 'IMDB URI', 'Rotten Tomatoes URI',
                      'Letterboxd URI', 'Date Added']
# Generate header-attribute dictionaries and native csv header
csv_to_attr = dict(zip(csv_header_columns, movie_attributes))
attr_to_csv = dict(zip(movie_attributes, csv_header_columns))
csv_header = ''.join([x+',' for x in csv_header_columns]).rstrip(',')
# csv headers for conversion
letterboxd_headers = [
    'Date,Name,Year,Letterboxd URI',
    'Date,Name,Year,Letterboxd URI,Rating,Tags,Watched Date'
]
# Color settings
style_title = Fore.GREEN + Style.BRIGHT
style_attributes = Style.BRIGHT
style_number = Style.BRIGHT
style_search_results = Fore.YELLOW

class Movie(ListItem):
    def __init__(self, name='Movie Name', year=datetime.date.today().year):
        super().__init__()
        self.name = name
        self.year = int(year)
        self.date_watched = datetime.date(datetime.MINYEAR, 1, 1)
        self.rating = -1
        self.max_rating = 10
        self.letterboxd_URI = ''
        self.imdb_URI = ''
        self.rtomatoes_URI = ''

    def __str__(self):
        # Compute the number of spaces to pad with
        nspaces = len(str(self.id)) + 2
        padding = ''.join([' ' for i in range(nspaces)])
        s = [
            style_number + str(self.id),
            ') ' + Style.RESET_ALL,
            style_title + self.name + Fore.RESET,
            '\n' + padding + style_attributes + 'Year: ' + Style.RESET_ALL,
            str(self.year),
            '\n'
        ]
        if self.rating >= 0:
            s.append(padding + style_attributes + 'Rating: '  + Style.RESET_ALL
                     + str(10.0 * self.rating / self.max_rating) + '/10\n')
        if self.tags:
            s.append(padding + style_attributes + 'Tags: ' + Style.RESET_ALL)
            [s.append(str(x)+', ') for x in self.tags]
            s.append('\b\b  \n')
        if self.date_watched != datetime.date(1,1,1):
            s.append(padding + style_attributes + 'Watched on: '
                     + Style.RESET_ALL + str(self.date_watched) + '\n')
        if self.imdb_URI:
            s.append(padding + style_attributes + 'IMDB URI: '
                     + Style.RESET_ALL + str(self.imdb_URI) + '\n')
        if self.rtomatoes_URI:
            s.append(padding + style_attributes + 'Rotten Tomatoes URI: '
                     + Style.RESET_ALL + str(self.rtomatoes_URI) + '\n')
        if self.letterboxd_URI:
            s.append(padding + style_attributes + 'Letterboxd URI: '
                     + Style.RESET_ALL + str(self.letterboxd_URI) + '\n')
        s.append(padding + style_attributes + 'Added on: ' + Style.RESET_ALL
                 + str(self.date_added) + '\n')
        return ''.join(s)

    def to_csv_str(self):
        s = []
        s.append('"' + self.name + '"' + ',')
        s.append(str(self.year) + ',')
        if self.rating >= 0:
            s.append(str(self.rating))
        s.append(',')
        s.append(str(self.max_rating) + ',')
        if self.tags and self.tags[0]:
            s.append('"')
            [s.append(str(x)+',') for x in self.tags]
            s[-1] = s[-1].rstrip(',')
            s.append('"')
        s.append(',')
        if self.date_watched != datetime.date(1,1,1):
            s.append(str(self.date_watched))
        s.append(',')
        s.append(str(self.imdb_URI) + ',')
        s.append(str(self.rtomatoes_URI) + ',')
        s.append(str(self.letterboxd_URI) + ',')
        if self.date_added != datetime.date(1,1,1):
            s.append(str(self.date_added))
        return ''.join(s)

    def read_from_user(self):
        """Read the attributes of the new movie object from standard input.
        """
        print('Enter new movie details')
        # Name
        self.name = input('Name: ')
        # Year
        while True:
            try:
                self.year = int(input('Year released: '))
                if (self.year < datetime.MINYEAR
                    or self.year > datetime.MAXYEAR):
                    raise ValueError()
                break
            except ValueError:
                print('Year must be an integer between '
                      + str(datetime.MINYEAR) + ' and '
                      + str(datetime.MAXYEAR))
        # Date watched
        while True:
            try:
                s = input('Date watched [unwatched]:')
                if s:
                    self.date_watched = date_from_str(s)
                break
            except ValueError:
                print('Enter date in YYYY-MM-DD format')
        # Rating
        while True:
            try:
                s = input('Rating[/Max rating] [unrated]: ')
                if s:
                    sub_s = s.split('/')
                    self.rating = float(sub_s[0])
                    if len(sub_s) > 1:
                        self.max_rating = float(sub_s[1])
                    else:
                        self.max_rating = 10
                else:
                    self.rating = -1
                break
            except ValueError:
                print('Rating must be a number')
        # Tags
        s = input('Tags (comma separated): ')
        self.tags_from_str(s)
        # Automatically generated
        self.imdb_URI = get_imdb_URI(self.name, self.year)
        self.rtomatoes_URI = get_rtomatoes_URI(self.name, self.year)
        self.letterboxd_URI = get_letterboxd_URI(self.name, self.year)

    def edit_from_user(self):
        """Read the attributes of the movie object from standard input.
        """
        print('Change movie details')
        # Name
        s = input('Name [' + self.name +  ']: ')
        if s:
            self.name = s
        # Year
        while True:
            try:
                s = input('Year released [' + str(self.year) + ']: ')
                if s:
                    self.year = int(s)
                    if (self.year < datetime.MINYEAR
                        or self.year > datetime.MAXYEAR):
                        raise ValueError()
                    else:
                        break
                else:
                    break
            except ValueError:
                print('Year must be an integer between '
                      + str(datetime.MINYEAR) + ' and '
                      + str(datetime.MAXYEAR))
        # Date watched
        while True:
            try:
                if self.date_watched == datetime.date(datetime.MINYEAR, 1, 1):
                    s = input('Date watched [unwatched]:')
                else:
                    s = input('Date watched [' + str(self.date_watched) + ']:')
                if s:
                    self.date_watched = date_from_str(s)
                break
            except ValueError:
                print('Enter date in YYYY-MM-DD format')
        # Rating
        while True:
            try:
                if self.rating < 0:
                    s = input('Rating [unrated]: ')
                else:
                    s = input('Rating [' + str(self.rating) + '/' 
                              + str(self.max_rating) + ']: ')
                if s:
                    sub_s = s.split('/')
                    self.rating = float(sub_s[0])
                    if len(sub_s) > 1:
                        self.max_rating = float(sub_s[1])
                    else:
                        self.max_rating = 10
                break
            except ValueError:
                print('Rating must be a number')
        # Tags
        taglist = []
        [taglist.append(str(x)+', ') for x in self.tags]
        tagstr = ''.join(taglist)
        tagstr = tagstr.rstrip(', ')
        s = input('Tags [' + tagstr + ']: ')
        if s:
            self.tags_from_str(s)
        # IMDB URI
        s = input('IMDB URI [' + self.imdb_URI +  ']: ')
        if s:
            self.imdb_URI = s
        # Rotten Tomatoes URI
        s = input('Rotten Tomatoes URI [' + self.rtomatoes_URI +  ']: ')
        if s:
            self.rtomatoes_URI = s
        # Letterboxd URI
        s = input('Letterboxd URI [' + self.letterboxd_URI +  ']: ')
        if s:
            self.letterboxd_URI = s

    def write(self, fname, mode='a'):
        if (mode == 'w'):
            write_header = True
        else:
            # Only allow 'w' and 'a' file modes
            mode = 'a'
            # Test if file is empty
            try:
                with open(os.path.expanduser(fname), 'r') as f:
                    first_char = f.read(1)
                    if first_char:
                        write_header = False
                    else:
                        write_header = True
            except FileNotFoundError:
                write_header = True

        # Write file
        try:
            with open(os.path.expanduser(fname), mode) as f:
                if write_header:
                    f.write(csv_header + '\n')
                f.write(self.to_csv_str() + '\n')
        except FileNotFoundError:
            print('Could not open file ' + str(fname) + ' for writing')


class Movies(ListItems):
    def __str__(self):
        s = [str(x)+'\n' for x in self.list]
        return ''.join(s)

    def read(self, fname):
        with open(fname, newline='') as f:
            reader = csv.reader(f)
            try:
                # Skip first line
                header = next(reader)
                for row in reader:
                    
                    rating = row[header.index(attr_to_csv['rating'])]
                    max_rating = row[header.index(attr_to_csv['max_rating'])]
                    tags = row[header.index(attr_to_csv['tags'])]
                    date_watched \
                        = row[header.index(attr_to_csv['date_watched'])]
                    imdb_URI = row[header.index(attr_to_csv['imdb_URI'])]
                    rtomatoes_URI \
                        = row[header.index(attr_to_csv['rtomatoes_URI'])]
                    letterboxd_URI \
                        = row[header.index(attr_to_csv['letterboxd_URI'])]
                    if len(row) == len(attr_to_csv):
                        date_added \
                            = row[header.index(attr_to_csv['date_added'])]
                    else:
                        date_added = ''

                    self.list.append(Movie())
                    # ID
                    self.list[-1].id = len(self.list)
                    # Name
                    self.list[-1].name = row[header.index(attr_to_csv['name'])]
                    # Year
                    self.list[-1].year \
                        = int(row[header.index(attr_to_csv['year'])])
                    # Rating
                    if rating:
                        self.list[-1].rating = float(rating)
                    # Max rating
                    if max_rating:
                        self.list[-1].max_rating = float(max_rating)
                    # Tags
                    if tags:
                        # Split tag string to individual tags
                        self.list[-1].tags_from_str(tags)
                    # Date watched
                    if date_watched:
                        dt = date_watched.split('-')
                        self.list[-1].date_watched = datetime.date(
                            int(dt[0]),
                            int(dt[1]),
                            int(dt[2])
                        )
                    else:
                        # Otherwise set the minimum available date
                        self.list[-1].date_watched = datetime.date(
                            datetime.MINYEAR,
                            1,
                            1
                        )
                    # IMDB URI
                    if imdb_URI:
                        self.list[-1].imdb_URI = imdb_URI
                    else:
                        self.list[-1].imdb_URI \
                          = get_imdb_URI(self.list[-1].name,
                                         self.list[-1].year)
                    # Rotten Tomatoes URI
                    if rtomatoes_URI:
                        self.list[-1].rtomatoes_URI = rtomatoes_URI
                    else:
                        self.list[-1].rtomatoes_URI \
                          = get_rtomatoes_URI(self.list[-1].name,
                                              self.list[-1].year)
                    # Letterboxd URI
                    if letterboxd_URI:
                        self.list[-1].letterboxd_URI = letterboxd_URI
                    else:
                        self.list[-1].letterboxd_URI \
                          = get_letterboxd_URI(self.list[-1].name,
                                               self.list[-1].year)
                    # Date added
                    if date_added:
                        dt = date_added.split('-')
                        self.list[-1].date_added = datetime.date(
                            int(dt[0]),
                            int(dt[1]),
                            int(dt[2])
                        )
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fname,
                                                       reader.line_num, e))

    def write(self, fname, mode='a'):
        if (mode == 'w'):
            write_header = True
        else:
            # Only allow 'w' and 'a' file modes
            mode = 'a'
            # Test if file is empty
            try:
                with open(os.path.expanduser(fname), 'r') as f:
                    first_char = f.read(1)
                    if first_char:
                        write_header = False
                    else:
                        write_header = True
            except FileNotFoundError:
                write_header = True

        # Write file
        try:
            with open(os.path.expanduser(fname), mode) as f:
                if write_header:
                    f.write(csv_header + '\n')
                [f.write(item.to_csv_str() + '\n') for item in self.list]
        except FileNotFoundError:
            print('Could not open file ' + str(fname) + ' for writing')

    def import_data(self, fname):
        with open(fname, newline='') as f:
            reader = csv.reader(f)
            try:
                # Detect file origin from the header
                header = next(f).rstrip('\r\n')
                if (header == csv_header):
                    print('File already in correct format, conversion aborted')
                elif (header == letterboxd_headers[0]
                    or header == letterboxd_headers[1]):
                    # Letterboxd
                    for row in reader:
                        # Name and year
                        self.list.append(Movie(row[1], row[2]))
                        # ID
                        self.list[-1].id = len(self.list)
                        # Date added
                        dt = row[0].split('-')
                        self.list[-1].date_added = datetime.date(
                            int(dt[0]),
                            int(dt[1]),
                            int(dt[2])
                        )
                        # Rating
                        if len(row) >= 5 and row[4]:
                            self.list[-1].rating = float(row[4])
                        # Tags
                        if len(row) >= 6 and row[5]:
                            # Split tag string to individual tags
                            self.list[-1].tags_from_str(row[5])
                        # Date watched if available
                        if len(row) >= 7 and row[6]:
                            dt = row[6].split('-')
                            self.list[-1].date_watched = datetime.date(
                                int(dt[0]),
                                int(dt[1]),
                                int(dt[2])
                            )
                        else:
                            # Otherwise set the minimum available year
                            self.list[-1].date_watched = datetime.date(
                                datetime.MINYEAR,
                                1,
                                1
                            )
                        # Letterboxd URI
                        if row[3]:
                            self.list[-1].letterboxd_URI = row[3]
                        else:
                            self.list[-1].letterboxd_URI \
                              = get_letterboxd_URI(self.list[-1].name,
                                                   self.list[-1].year)
                        # Rotten Tomatoes URI
                        self.list[-1].rtomatoes_URI \
                          = get_rtomatoes_URI(self.list[-1].name,
                                              self.list[-1].year)
                        # IMDB URI
                        self.list[-1].imdb_URI \
                          = get_imdb_URI(self.list[-1].name,
                                         self.list[-1].year)
                else:
                    print('Unknown csv header, conversion aborted')
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fname,
                                                       reader.line_num, e))


def get_letterboxd_URI(name, year):
    """Given a string s containing a movie name, return a string containing the
    Letterboxd URI that corresponds to that movie.
    """
    # Keep only letters, numbers and spaces
    name_letterboxd = ''.join([c for c in name if c.isalnum() or c.isspace()])
    # Make all letters lower case
    name_letterboxd = name_letterboxd.lower()
    # Replace spaces with dashes
    name_letterboxd = name_letterboxd.replace(' ', '-')
    # Remove consecutive dashes
    name_letterboxd = name_letterboxd.replace('--', '-')
    # TODO Check whether two movies of the same name exist and select the one
    # with the correct year. Add a dash to the end of the URI followed by the
    # year. Also check for +-1 year.
    uri = 'https://letterboxd.com/film/' + name_letterboxd
    return uri


def get_rtomatoes_URI(name, year):
    """Given a string s containing a movie name, return a string containing the
    Rotten Tomatoes URI that corresponds to that movie.
    """
    # Keep only letters, numbers and spaces
    name_rtomatoes = ''.join([c for c in name if c.isalnum() or c.isspace()])
    # Make all letters lower case
    name_rtomatoes = name_rtomatoes.lower()
    # Replace spaces with underscores
    name_rtomatoes = name_rtomatoes.replace(' ', '_')
    # Remove consecutive underscores
    name_rtomatoes = name_rtomatoes.replace('__', '_')
    # TODO Check whether two movies of the same name exist and select the one
    # with the correct year. Add an underscore to the end of the URI followed
    # by the year. Also check for +-1 year.
    uri = 'https://www.rottentomatoes.com/m/' + name_rtomatoes
    return uri


def get_imdb_URI(name, year):
    # TODO
    return ''


