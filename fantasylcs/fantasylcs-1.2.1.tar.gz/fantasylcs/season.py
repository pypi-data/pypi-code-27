#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

FANTASY_SEASON_START = 1
FANTASY_SEASON_CURRENT = 16
REGIONS_SUPPORTED = ["na", "lan", "las", "euw", "eune", "oce"]


class SeasonDataException(Exception):
    """Handles SeasonData Exceptions"""


class SeasonData:
    """Handles Season Data requests"""

    def __init__(self, region, season):
        self.season_data = self._fetch_season_data(region, int(season))

    def _fetch_season_data(self, region, season):
        """
        Returns fetched season data

        @param region - region that fantasy season exists in
        @param season - fantasy lcs season number
                        (don't confuse this with the season number of LoL)
        """
        try:
            region = region.lower()
            if region not in REGIONS_SUPPORTED:
                raise Exception("Region not supported: {}"
                                "".format(region))
            if not FANTASY_SEASON_START <= season <= FANTASY_SEASON_CURRENT:
                raise Exception("Season does not exist")
            FANTASY_SEASON_URL = ("https://fantasy.{}.lolesports.com/en-US/api/"
                                  "season/{}".format(region, season))
            data = requests.get(FANTASY_SEASON_URL)
            data.raise_for_status()
            return data.json()
        except Exception as e:
            error_msg = ("Failed to retrieve fantasy season data: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_season_data(self):
        """
        Returns season data
        """
        try:
            return self.season_data
        except Exception as e:
            error_msg = ("Failed to retrieve season data: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_number_of_weeks(self):
        """
        Returns the number of weeks there are during the fantasy
        season
        """
        try:
            return self.season_data["numberOfWeeks"]
        except Exception as e:
            error_msg = ("Failed to retrieve number of weeks: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_matches(self):
        """
        Returns a list of all the matches played during the lcs
        """
        try:
            return self.season_data["proMatches"]
        except Exception as e:
            error_msg = ("Failed to retrieve all matches: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_players(self):
        """
        Returns a list of all the players in lcs
        """
        try:
            return self.season_data["proPlayers"]
        except Exception as e:
            error_msg = ("Failed to retrieve all players: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_teams(self):
        """
        Returns a list of all the teams in lcs
        """
        try:
            return self.season_data["proTeams"]
        except Exception as e:
            error_msg = ("Failed to retrieve all teams: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_roster_locks(self):
        """
        Returns a dict of the times when rosters get locked in
        for the week
        """
        try:
            return self.season_data["rosterLocksByWeek"]
        except Exception as e:
            error_msg = ("Failed to retrieve all roster locks: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_roster_trends_status(self):
        """
        Returns true if roster trends are disabled
        false if roster trends are enabled
        """
        try:
            return self.season_data["rosterTrendsDisabled"]
        except Exception as e:
            error_msg = ("Failed to retrieve roster trend status: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_season_start_time(self):
        """
        Returns the time when the fantasy season begins
        """
        try:
            return self.season_data["seasonBegins"]
        except Exception as e:
            error_msg = ("Failed to retrieve season start time: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_season_end_time(self):
        """
        Returns the time when the fantasy season ends
        """
        try:
            return self.season_data["seasonEnds"]
        except Exception as e:
            error_msg = ("Failed to retrieve season end time: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_season_name(self):
        """
        Returns the season name
        """
        try:
            return self.season_data["seasonName"]
        except Exception as e:
            error_msg = ("Failed to retrieve season name: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_season_split(self):
        """
        Returns the season split
        """
        try:
            return self.season_data["seasonSplit"]
        except Exception as e:
            error_msg = ("Failed to retrieve season split: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_season_stats(self):
        """
        Returns a dict of all the stats available
        """
        try:
            return self.season_data["stats"]
        except Exception as e:
            error_msg = ("Failed to retrieve all season stats: {}"
                         "".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_actual_player_stats(self):
        """
        Returns a list of all the actual player stats available
        """
        try:
            return self.season_data["stats"]["actualPlayerStats"]
        except Exception as e:
            error_msg = ("Failed to retrieve all of the actual player stats: "
                         "{}".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_actual_team_stats(self):
        """
        Returns a list of all the actual team stats available
        """
        try:
            return self.season_data["stats"]["actualTeamStats"]
        except Exception as e:
            error_msg = ("Failed to retrieve all of the actual team stats: "
                         "{}".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_projected_player_stats(self):
        """
        Returns a list of all the projected player stats available
        """
        try:
            return self.season_data["stats"]["projectedPlayerStats"]
        except Exception as e:
            error_msg = ("Failed to retrieve all of the projected player "
                         "stats: {}".format(str(e)))
            raise SeasonDataException(error_msg)

    def get_all_projected_team_stats(self):
        """
        Returns a list of all the projected team stats available
        """
        try:
            return self.season_data["stats"]["projectedTeamStats"]
        except Exception as e:
            error_msg = ("Failed to retrieve all of the projected team stats: "
                         "{}".format(str(e)))
            raise SeasonDataException(error_msg)
