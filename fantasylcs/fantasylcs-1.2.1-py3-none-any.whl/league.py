#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


REGIONS_SUPPORTED = ["na", "lan", "las", "euw", "eune", "oce"]


class FantasyLeagueException(Exception):
    """Handles FantasyLeague Exceptions"""


class FantasyLeague:
    """Handles fantasy requests"""

    def __init__(self, region, fantasy_league_id):
        self.data = self._get_fantasy_data(region, fantasy_league_id)

    def _get_fantasy_data(self, region, fantasy_league_id):
        """
        Returns data of fantasy league

        @param region - region that fantasy league exists in
        @param fantasy_league_id - id of the fantasy league to search for
        """
        try:
            region = region.lower()
            if region not in REGIONS_SUPPORTED:
                raise Exception("Region not supported: {}"
                                "".format(region))
            FANTASY_URL = ("https://fantasy.{}.lolesports.com/en-US/api/"
                           "league/{}".format(region, fantasy_league_id))
            data = requests.get(FANTASY_URL)
            data.raise_for_status()
            return data.json()
        except Exception as e:
            error_msg = ("Failed to retrieve name of fantasy league: {}"
                         "".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_id(self):
        """
        Returns the fantasy league id
        """
        try:
            return self.data["id"]
        except Exception as e:
            error_msg = ("Failed to retrieve id of fantasy league: {}"
                         "".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_name(self):
        """
        Returns the name of the fantasy league
        """
        try:
            return self.data["name"]
        except Exception as e:
            error_msg = ("Failed to retrieve name of fantasy league: {}"
                         "".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_size(self):
        """
        Returns the number of teams in the fantasy league
        """
        try:
            return self.data["size"]
        except Exception as e:
            error_msg = ("Failed to retrieve the size of the fantasy "
                         "league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_current_week(self):
        """
        Returns the current week number in the fantasy league
        """
        try:
            return self.data["currentWeek"]
        except Exception as e:
            error_msg = ("Failed to retrieve current week of the "
                         "fantasy league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_ignored_weeks(self):
        """
        Returns the total number of weeks ignored in the
        fantasy league
        """
        try:
            return self.data["ignoredWeeks"]
        except Exception as e:
            error_msg = ("Failed to retrieve count of ignored weeks: "
                         "{}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_status(self):
        """
        Returns the status of the fantasy league
        """
        try:
            return self.data["status"]
        except Exception as e:
            error_msg = ("Failed to retrieve status of fantasy league: {}"
                         "".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_games_counted(self):
        """
        Returns the mode of what games count towards fantasy
        """
        try:
            return self.data["gamesCounted"]
        except Exception as e:
            error_msg = ("Failed to retrieve game mode of fantasy league: {}"
                         "".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_points_per_stat(self):
        """
        Returns a dictionary of stats with how many points counted
        per stat
        """
        try:
            return self.data["pointsPerStat"]
        except Exception as e:
            error_msg = ("Failed to retrieve status of fantasy league: {}"
                         "".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_teams(self):
        """
        Returns a list of fantasy teams
        """
        try:
            return self.data["fantasyTeams"]
        except Exception as e:
            error_msg = ("Failed to retrieve fantasy teams of fantasy league: "
                         "{}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_matches(self):
        """
        Returns a list of all the fantasy matches
        """
        try:
            return self.data["fantasyMatches"]
        except Exception as e:
            error_msg = ("Failed to retrieve fantasy matches of fantasy "
                         "league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_roster_updates(self):
        """
        Returns a list of all the roster updates
        """
        try:
            return self.data["fantasyRosterUpdates"]
        except Exception as e:
            error_msg = ("Failed to retrieve fantasy roster updates of "
                         "fantasy league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_trades(self):
        """
        Returns a list of all the trades made
        """
        try:
            return self.data["trades"]
        except Exception as e:
            error_msg = ("Failed to retrieve trades of fantasy "
                         "league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_roster_limits(self):
        """
        Returns the number limit of the roles you're
        allowed to have
        """
        try:
            return self.data["rosterShape"]
        except Exception as e:
            error_msg = ("Failed to retrieve trades of fantasy "
                         "league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_fantasy_role_limit(self):
        """
        Returns the number limit of the same role you're
        allowed to have
        """
        try:
            return self.data["positionCap"]
        except Exception as e:
            error_msg = ("Failed to retrieve position limit of fantasy "
                         "league: {}".format(str(e)))
            raise FantasyLeagueException(error_msg)

    def get_predraft_phase(self):
        """
        Returns predraft phase
        True if league still needs to draft
        False if players already drafted
        """
        try:
            return self.data["predraft"]
        except Exception as e:
            error_msg = ("Failed to retrieve predraft phase: "
                         "{}".format(str(e)))
            raise FantasyLeagueException(error_msg)
