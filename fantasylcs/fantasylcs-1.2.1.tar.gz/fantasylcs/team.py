class TeamDataException(Exception):
    """Handles TeamData Exceptions"""


class TeamData:
    """Handles Team Data requests"""

    def __init__(self, season, team):
        self.profile_data = self._get_profile(season, team)
        self.match_data = self._get_match_data(season)
        self.projected_data = self._get_projected_data(season)

    def _get_profile(self, season, team):
        """
        Returns profile data of the team

        @param team - id or name of the team to look up
        """
        try:
            try:
                team = int(team)
            except ValueError:
                team = team.lower()
            team_list = season.get_season_data()["proTeams"]
            for t in team_list:
                if t["id"] == team:
                    return t
                if t["name"].lower() == team:
                    return t
        except Exception as e:
            error_msg = ("Failed to retrieve team profile data: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def _get_match_data(self, season):
        """
        Returns match data related to team
        """
        try:
            match_data = []
            team_id = self.profile_data["id"]
            matches = season.get_season_data()["stats"]["actualTeamStats"]
            for match in matches:
                if team_id == match[0]:
                    match_data.append(match)
            return match_data
        except Exception as e:
            error_msg = ("Failed to retrieve team match data: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def _get_projected_data(self, season):
        """
        Returns projected match data related to team
        """
        try:
            match_data = []
            team_id = self.profile_data["id"]
            matches = season.get_season_data()["stats"]["projectedTeamStats"]
            for match in matches:
                if team_id == match[0]:
                    match_data.append(match)
            return match_data
        except Exception as e:
            error_msg = ("Failed to retrieve projected team data: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_team_id(self):
        """
        Returns the team id
        """
        try:
            return self.profile_data["id"]
        except Exception as e:
            error_msg = ("Failed to retrieve team id: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_name(self):
        """
        Returns the team name
        """
        try:
            return self.profile_data["name"]
        except Exception as e:
            error_msg = ("Failed to retrieve team name: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_acronym(self):
        """
        Returns the acronym of the team name
        """
        try:
            return self.profile_data["shortName"]
        except Exception as e:
            error_msg = ("Failed to retrieve team name: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_region(self):
        """
        Returns the region of the team
        """
        try:
            return self.profile_data["league"]
        except Exception as e:
            error_msg = ("Failed to retrieve region: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_positions(self):
        """
        Returns a list of all the team's positions
        """
        try:
            return self.profile_data["positions"]
        except Exception as e:
            error_msg = ("Failed to retrieve a list of team positions: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_riot_id(self):
        """
        Returns the team's riot id
        """
        try:
            return self.profile_data["riotId"]
        except Exception as e:
            error_msg = ("Failed to retrieve the team's riot id: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_trends_by_week(self):
        """
        Returns a dictionary of all the team's weekly trends
        """
        try:
            return self.profile_data["trendsByWeek"]
        except Exception as e:
            error_msg = ("Failed to retrieve weekly trends: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_matches_played(self):
        """
        Returns the total matches played
        """
        try:
            return len(self.match_data)
        except Exception as e:
            error_msg = ("Failed to retrieve number of matches played: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_all_match_stats(self):
        """
        Returns a list of all matches played by the team
        """
        try:
            return self.match_data
        except Exception as e:
            error_msg = ("Failed to retrieve all match stats: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_match_stats(self, match_number):
        """
        Returns match stats of a team given a number in a range
        from the first match to the most recent match

        @param match_number - # of the match to get
        """
        try:
            match_number = int(match_number)
            if not 0 <= match_number < len(self.match_data):
                raise Exception("Specified number is out of the match range: "
                                "{}".format(match_number))
            match_stats = self.match_data[match_number]
            return match_stats
        except Exception as e:
            error_msg = ("Failed to retrieve match stats: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_all_projected_stats(self):
        """
        Returns a list of all projected matches to be played by
        the team
        """
        try:
            return self.projected_data
        except Exception as e:
            error_msg = ("Failed to retrieve all projected stats: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)

    def get_projected_stats(self, match_number):
        """
        Returns projected stats of a team given a number in a range
        from the first match to the most recent match

        @param match_number - # of the match to get
        """
        try:
            projected_number = int(match_number)
            if not 0 <= projected_number < len(self.projected_data):
                raise Exception("Specified number is out of the match range: "
                                "{}".format(match_number))
            projected_stats = self.projected_data[match_number]
            return projected_stats
        except Exception as e:
            error_msg = ("Failed to retrieve match stats: {}"
                         "".format(str(e)))
            raise TeamDataException(error_msg)
