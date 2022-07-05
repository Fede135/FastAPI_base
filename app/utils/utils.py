import datetime
from typing import List

from fastapi import HTTPException

from app.utils.constants import FOOTBALL_URL
from app.utils.football_api_proxy import Proxy
from app.utils import utils
from sql_app.models import Player


def load_players(team_id: str, proxy: Proxy) -> List[Player]:

    teams_url = get_api_footbal_url() + 'teams/{}'.format(team_id)
    squad = get_squad_from_team_url(teams_url, proxy)

    # Hack to hit v4 of football_api, in lot of cases API v2 return with squad empty.
    # I detect that squad is returning empty in v2
    if not squad:
        teams_url = get_api_footbal_url('v4') + 'teams/{}'.format(team_id)
        squad = get_squad_from_team_url(teams_url, proxy)

    db_player_list = []

    for player in squad:
        date_of_birth = None
        country_of_birth = None

        if player.get('dateOfBirth'):
            date_of_birth = utils.format_date_of_birth_players(player.get('dateOfBirth'))

        # API v4 does not have countryOfBirth so we are replacing with nationality
        if not player.get('countryOfBirth', None):
            country_of_birth = player.get('nationality')

        db_player = Player(
            name=player.get('name'),
            position=player.get('position'),
            countryOfBirth=country_of_birth if country_of_birth else player.get('countryOfBirth'),
            dateOfBirth=date_of_birth,
            nationality=player.get('nationality'),
        )
        db_player_list.append(db_player)

    return db_player_list


def format_date_of_birth_players(str_date: str) -> datetime.date:
    try:
        converted_date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ").date()
    except ValueError:
        # Hack to hit v4. In lot of cases API v2 return with squad empty.
        # So we are hitting API v4 instead. API v4 returns dateOfBirth in %Y-%m-%d format
        # instead of %Y-%m-%dT%H:%M:%SZ as API v2
        converted_date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()

    return converted_date


def get_api_footbal_url(version='v2') -> str:
    return FOOTBALL_URL.format(version)


def get_squad_from_team_url(teams_url: str, proxy: Proxy):
    response = proxy.get(teams_url)
    if response.status_code < 200 or response.status_code > 299:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
    response_json = response.json()
    return response_json['squad']
