# -*- coding: utf-8 -*-
# :Project:   SoL -- Test /data/* views
# :Created:   lun 09 lug 2018 11:11:25 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Lele Gaifax
#

from sol.models import Club, Player, Rating, Tourney


def test_clubs(guest_user, session):
    response = guest_user.get_route('clubs')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == session.query(Club).count()


def test_clubs_metadata(guest_user):
    response = guest_user.get_route('clubs', _query={'metadata': 'metadata'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['metadata']['fields'][-1]['name'] == 'Owner'


def test_clubs_no_owner_metadata(guest_user):
    response = guest_user.get_route('clubs', _query={'metadata': 'metadata',
                                                     'only_cols': 'idclub,description'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert 'Owner' not in [f['name'] for f in result['metadata']['fields']]


def test_clubs_no_owner(guest_user):
    response = guest_user.get_route('clubs',
                                    _query={'only_cols': 'idclub,description,nationality'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert 'Owner' not in result['root'][0]


def test_club_by_description(guest_user, club_scr):
    response = guest_user.get_route('clubs',
                                    _query={'filter_by_description': club_scr.description})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    club = result['root'][0]
    assert club['description'] == club_scr.description
    assert club['Championships'] == 7
    assert club['Owner'] == 'Administrator'


def test_owned_club(guest_user, club_owned, user_lele):
    response = guest_user.get_route('clubs',
                                    _query={'filter_by_description': club_owned.description})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    club = result['root'][0]
    assert user_lele.firstname in club['Owner']


def test_federations(guest_user):
    response = guest_user.get_route('federations')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1


def test_owners(guest_user):
    response = guest_user.get_route('owners')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 2


def test_owners_metadata(guest_user):
    response = guest_user.get_route('owners', _query={'metadata': 'metadata'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['metadata']['fields'][-1]['name'] == 'Fullname'


def test_players(guest_user, session):
    response = guest_user.get_route('players')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == session.query(Player).count()
    for p in result['root']:
        if p['firstname'] == 'Fata':
            assert p['Language'] == 'Zulu'
            break
    else:
        assert False, "No Fata??"


def test_players_metadata(guest_user):
    response = guest_user.get_route('players', _query={'metadata': 'metadata'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert 'Language' in (f['name'] for f in result['metadata']['fields'])


def test_duplicated_players(guest_user):
    response = guest_user.get_route('players', _query={'dups': 1})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 4


def test_active_players(guest_user, session, club_scr):
    response = guest_user.get_route('players', _query={'played4club': club_scr.idclub})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert 1 < result['count'] < session.query(Player).count()


def test_player_by_nickname(guest_user, player_lele, tourney_rated_no_turns_odd,
                            tourney_closed):
    response = guest_user.get_route('players',
                                    _query={'filter_by_nickname': player_lele.nickname})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    player = result['root'][0]
    assert player['firstname'] == player_lele.firstname
    assert player['lastname'] == player_lele.lastname
    assert player['LastPlayed'] == tourney_closed.date.isoformat()


def test_owned_player(guest_user, player_fata, user_lele):
    response = guest_user.get_route('players',
                                    _query={'filter_by_firstname': player_fata.firstname,
                                            'filter_by_lastname': player_fata.lastname})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    player = result['root'][0]
    assert user_lele.firstname in player['Owner']


def test_championships(guest_user):
    response = guest_user.get_route('championships')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 10


def test_championship_by_description(guest_user, club_scr):
    response = guest_user.get_route('championships',
                                    _query={'filter_by_description': 'SCR 2010 (test)'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    championship = result['root'][0]
    assert championship['Club'] == club_scr.description


def test_owned_championship(guest_user, championship_current, user_lele):
    idc = championship_current.idchampionship
    response = guest_user.get_route('championships', _query={'filter_by_idchampionship': idc})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    championship = result['root'][0]
    assert user_lele.firstname in championship['Owner']


def test_tourneys(guest_user, session):
    response = guest_user.get_route('tourneys')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == session.query(Tourney).count()


def test_player_tourneys(guest_user, player_fata):
    response = guest_user.get_route('tourneys', _query={'idplayer': player_fata.idplayer})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 8


def test_tourney_by_description(guest_user, tourney_first, user_lele):
    td = tourney_first.description
    response = guest_user.get_route('tourneys', _query={'filter_by_description': td})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    tourney = result['root'][0]
    assert tourney['description'] == tourney_first.description
    assert tourney['date'] == tourney_first.date.isoformat()
    assert tourney['Championship'] == tourney_first.championship.description
    assert user_lele.firstname in tourney['Owner']


def test_countries(guest_user):
    response = guest_user.get_route('countries')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert set(result['root'][0].keys()) == set(['code', 'name'])


def test_languages(guest_user):
    response = guest_user.get_route('languages')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert set(result['root'][0].keys()) == set(['code', 'name'])


def test_ratings(guest_user, session, rating_european):
    response = guest_user.get_route('ratings')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == session.query(Rating).count()
    assert result['root'][0]['description'] == rating_european.description
    assert result['root'][0]['Players'] == 5
    assert result['root'][0]['Tourneys'] == 1


def test_rated_players(guest_user, rating_european, player_varechina):
    response = guest_user.get_route('rated_players',
                                    _query={'filter_by_idrating': rating_european.idrating})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 5
    assert result['root'][0]['lastname'] == player_varechina.lastname


def test_owned_rating(guest_user, rating_standalone, user_lele):
    rd = rating_standalone.description
    response = guest_user.get_route('ratings', _query={'filter_by_description': rd})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    rating = result['root'][0]
    assert user_lele.firstname in rating['Owner']


def test_users(guest_user):
    response = guest_user.get_route('users')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] == 1
    assert result['root'][0]['lastname'] == 'Gaifax'
