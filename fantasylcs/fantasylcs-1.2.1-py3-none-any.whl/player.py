class PlayerDataException(Exception):
    """Handles PlayerData Exceptions"""


class PlayerData:
    """Handles Player Data requests"""

    def __init__(self, season, player):
        self.profile_data = self._get_profile(season, player)
        self.match_data = self._get_match_data(season)
        self.projected_data = self._get_projected_data(season)

    def _get_profile(self, season, player):
        """
        Returns profile data of the player

        @param player - id or name of the player to look up
        """
        try:
            try:
                player = int(player)
            except ValueError:
                player = player.lower()
            player_list = season.get_season_data()["proPlayers"]
            for p in player_list:
                if p["id"] == player:
                    return p
                if p["name"].lower() == player:
                    return p
        except Exception as e:
            error_msg = ("Failed to retrieve player profile data: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def _get_match_data(self, season):
        """
        Returns match data related to player
        """
        try:
            match_data = []
            player_id = self.profile_data["id"]
            matches = season.get_season_data()["stats"]["actualPlayerStats"]
            for match in matches:
                if player_id == match[0]:
                    match_data.append(match)
            return match_data
        except Exception as e:
            error_msg = ("Failed to retrieve player match data: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def _get_projected_data(self, season):
        """
        Returns projected match data related to player
        """
        try:
            match_data = []
            player_id = self.profile_data["id"]
            matches = season.get_season_data()["stats"]["projectedPlayerStats"]
            for match in matches:
                if player_id == match[0]:
                    match_data.append(match)
            return match_data
        except Exception as e:
            error_msg = ("Failed to retrieve player match data: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_player_id(self):
        """
        Returns the player id
        """
        try:
            return self.profile_data["id"]
        except Exception as e:
            error_msg = ("Failed to retrieve player id: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_name(self):
        """
        Returns the player name
        """
        try:
            return self.profile_data["name"]
        except Exception as e:
            error_msg = ("Failed to retrieve player name: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_photo_url(self):
        """
        Returns the photo url of the player
        """
        try:
            return self.profile_data["photoUrl"]
        except Exception as e:
            error_msg = ("Failed to retrieve photo url: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_positions(self):
        """
        Returns a list of all the player's positions
        """
        try:
            return self.profile_data["positions"]
        except Exception as e:
            error_msg = ("Failed to retrieve a list of player positions: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_team_id(self):
        """
        Returns the player's team id
        """
        try:
            return self.profile_data["proTeamId"]
        except Exception as e:
            error_msg = ("Failed to retrieve the player's team id: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_riot_id(self):
        """
        Returns the player's riot id
        """
        try:
            return self.profile_data["riotId"]
        except Exception as e:
            error_msg = ("Failed to retrieve the player's riot id: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_trends_by_week(self):
        """
        Returns a dictionary of all the player's weekly trends
        """
        try:
            return self.profile_data["trendsByWeek"]
        except Exception as e:
            error_msg = ("Failed to retrieve weekly trends: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_matches_played(self):
        """
        Returns the total matches played
        """
        try:
            return len(self.match_data)
        except Exception as e:
            error_msg = ("Failed to retrieve number of matches played: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_all_match_stats(self):
        """
        Returns a list of all matches played by the player
        """
        try:
            return self.match_data
        except Exception as e:
            error_msg = ("Failed to retrieve all match stats: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_match_stats(self, match_number):
        """
        Returns match stats of a player given a number in a range
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
            raise PlayerDataException(error_msg)

    def get_all_projected_stats(self):
        """
        Returns a list of all projected matches to be played by
        the player
        """
        try:
            return self.projected_data
        except Exception as e:
            error_msg = ("Failed to retrieve all projected stats: {}"
                         "".format(str(e)))
            raise PlayerDataException(error_msg)

    def get_projected_stats(self, match_number):
        """
        Returns projected stats of a player given a number in a range
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
            raise PlayerDataException(error_msg)
