from unittest.mock import patch

import pytest
import sqlalchemy

from fastapi.testclient import TestClient

from app.main import app, get_db
from sql_app.crud import competition as crud_competition
from sql_app.crud import player as crud_player
from sql_app.crud import team as crud_team
from app.utils.football_api_proxy import Proxy
from sql_app.database import TestingSessionLocal, test_engine
from tests.utilities.utils import (
    mocked_requests_get,
)

from tests.utilities.utils import setup_test_database


# It creates a nested
# transaction, recreates it when the application code calls session.commit
# and rolls it back at the end.
# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
def session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@patch.object(Proxy, 'get', side_effect=mocked_requests_get)
def test_import_league_competition_and_teams(mock_get, client, session):
    expected_json_response = {
        "code": "PL",
        "id": 1,
        "name": "Premier League",
        "areaName": "England",
        "teams": [
            {
                "areaName": "England",
                "name": "Fulham FC",
                "shortName": "Fulham",
                "tla": "FUL",
                "email": "enquiries@fulhamfc.com"
            },
            {
                "areaName": "England",
                "name": "Nottingham Forest FC",
                "shortName": "Nottingham",
                "tla": "NOT",
                "email": None
            }
        ]
    }
    expected_status_response = 200
    expected_count_competition = 1
    expected_count_teams = 2
    expected_count_players = 4

    response = client.post(
        "/league/PL/import"
    )

    assert response.status_code == expected_status_response
    assert response.json() == expected_json_response

    assert expected_count_competition == crud_competition.get_count_competitions(session)
    assert expected_count_teams == crud_team.get_count_teams(session)
    assert expected_count_players == crud_player.get_count_players(session)


@patch.object(Proxy, 'get', side_effect=mocked_requests_get)
def test_import_league_competition_not_valid_api_perms(mock_get, client, session):
    expected_json_response = {
        "detail": {
            "message": "The resource you are looking for is restricted."
                       " Please pass a valid API token and check your subscription for permission.",
        }
    }
    expected_status_response = 403

    response = client.post(
        "/league/MLS/import"
    )

    assert response.status_code == expected_status_response
    assert response.json() == expected_json_response


@patch.object(Proxy, 'get', side_effect=mocked_requests_get)
def test_import_league_competition_not_exist(mock_get, client, session):
    expected_json_response = {
        "detail": {
            "message": "The resource you are looking for does not exist."
        }
    }
    expected_status_response = 404

    response = client.post(
        "/league/AA/import"
    )

    assert response.status_code == expected_status_response
    assert response.json() == expected_json_response


def test_get_players_from_league(client, session):

    setup_test_database(session)

    response = client.get(
        "/league/SL/players"
    )

    expected_status_response = 200

    expected_response = {
        "items": [
            {
                "name": "Marek Rodák",
                "position": "Goalkeeper",
                "dateOfBirth": "1996-12-13",
                "countryOfBirth": "Slovakia",
                "nationality": "Slovakia"
            },
            {
                "name": "Fábio Carvalho",
                "position": None,
                "dateOfBirth": "2022-06-30",
                "countryOfBirth": "England",
                "nationality": "England",
            },
            {
                "name": "Ethan Horvath",
                "position": "Goalkeeper",
                "dateOfBirth": "1995-06-09",
                "countryOfBirth": "United States",
                "nationality": "United States",
            }
        ],
        "total": 3,
        "page": 1,
        "size": 50
    }

    assert response.status_code == expected_status_response
    assert response.json() == expected_response


def test_get_players_from_league_filter_team(client, session):

    setup_test_database(session)

    response_1 = client.get(
        "/league/SL/players?team_name=Team1"
    )

    response_2 = client.get(
        "/league/TL/players?team_name=Team2"
    )

    expected_status_response = 200

    expected_response_1 = {
        "items": [
            {
                "name": "Marek Rodák",
                "position": "Goalkeeper",
                "dateOfBirth": "1996-12-13",
                "countryOfBirth": "Slovakia",
                "nationality": "Slovakia"
            },
            {
                "name": "Fábio Carvalho",
                "position": None,
                "dateOfBirth": "2022-06-30",
                "countryOfBirth": "England",
                "nationality": "England",
            },
        ],
        "total": 2,
        "page": 1,
        "size": 50
    }

    expected_response_2 = {
        "items": [
            {
                "name": "Brice Samba",
                "position": "Goalkeeper",
                "dateOfBirth": "1994-04-25",
                "countryOfBirth": "Congo",
                "nationality": "Congo"
            }
        ],
        "total": 1,
        "page": 1,
        "size": 50
    }

    assert response_1.status_code == expected_status_response
    assert response_1.json() == expected_response_1
    assert response_2.json() == expected_response_2


def test_get_players_from_league_filter_pagination(client, session):

    setup_test_database(session)

    response = client.get(
        "/league/SL/players?size=1&page=3"
    )

    expected_status_response = 200

    expected_response = {
        "items": [
            {
                "name": "Ethan Horvath",
                "position": "Goalkeeper",
                "dateOfBirth": "1995-06-09",
                "countryOfBirth": "United States",
                "nationality": "United States",
            }
        ],
        "total": 3,
        "page": 3,
        "size": 1
    }

    assert response.status_code == expected_status_response
    assert response.json() == expected_response


def test_get_players_league_no_exist(client):

    response = client.get(
        "/league/FAKE/players"
    )

    expected_status_response = 404
    expected_response = {'detail': 'League FAKE not found'}

    assert response.status_code == expected_status_response
    assert response.json() == expected_response
