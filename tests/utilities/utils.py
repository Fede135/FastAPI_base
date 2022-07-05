from datetime import date

from sql_app.models import Competition, Player, Team


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


test_team_list = [
    {
        "id": 63,
        "area": {
            "id": 2072,
            "name": "England"
        },
        "name": "Fulham FC",
        "shortName": "Fulham",
        "tla": "FUL",
        "email": "enquiries@fulhamfc.com",
    },
    {
        "id": 351,
        "area": {
            "id": 2072,
            "name": "England"
        },
        "name": "Nottingham Forest FC",
        "shortName": "Nottingham",
        "tla": "NOT",
        "email": None,
    },
]

test_squad_63 =[
    {

        "name": "Marek Rodák",
        "position": "Goalkeeper",
        "dateOfBirth": "1996-12-13T00:00:00Z",
        "countryOfBirth": "Slovakia",
        "nationality": "Slovakia",
    },
    {
        "name": "Fábio Carvalho",
        "position": None,
        "dateOfBirth": "2022-06-30T00:00:00Z",
        "countryOfBirth": None,
        "nationality": "England",
    }
]

test_squad_351 = [
    {
        "name": "Brice Samba",
        "position": "Goalkeeper",
        "dateOfBirth": "1994-04-25T00:00:00Z",
        "countryOfBirth": "Congo",
        "nationality": "Congo",
    },
    {
        "name": "Ethan Horvath",
        "position": "Goalkeeper",
        "dateOfBirth": "1995-06-09T00:00:00Z",
        "countryOfBirth": "United States",
        "nationality": "United States",
    },
]


def mocked_requests_get(*args, **kwargs):
    if args[0] == "https://api.football-data.org/v2/competitions/PL/teams":
        return MockResponse({
            "competition": {
                "area": {
                     "id": 2072,
                     "name": "England"
                },
                "name": "Premier League",
                "code": "PL"
            },
            "teams": test_team_list
        }, 200)
    if args[0] == "https://api.football-data.org/v2/teams/63":
        return MockResponse({
            "squad": test_squad_63
        }, 200)
    if args[0] == "https://api.football-data.org/v2/teams/351":
        return MockResponse({
            "squad": test_squad_351
        }, 200)
    if args[0] == "https://api.football-data.org/v2/competitions/MLS/teams":
        return MockResponse({
            "message": "The resource you are looking for is restricted."
                       " Please pass a valid API token and check your subscription for permission.",
        }, 403)
    if args[0] == "https://api.football-data.org/v2/competitions/AA/teams":
        return MockResponse({
            "message": "The resource you are looking for does not exist.",
        }, 404)


def setup_test_database(test_db):
    db_player_1 = Player(
        name="Marek Rodák",
        position="Goalkeeper",
        dateOfBirth=date(1996, 12, 13),
        countryOfBirth="Slovakia",
        nationality="Slovakia",
    )

    db_player_2 = Player(
        name="Fábio Carvalho",
        position=None,
        dateOfBirth=date(2022, 6, 30),
        countryOfBirth="England",
        nationality="England",
    )

    db_player_3 = Player(
        name="Brice Samba",
        position="Goalkeeper",
        dateOfBirth=date(1994, 4, 25),
        countryOfBirth="Congo",
        nationality="Congo",
    )

    db_player_4 = Player(
        name="Ethan Horvath",
        position="Goalkeeper",
        dateOfBirth=date(1995, 6, 9),
        countryOfBirth="United States",
        nationality="United States",
    )

    db_team_1 = Team(
        name="Team 1",
        tla="T1",
        shortName="Team1",
        areaName="Argentina",
        email="team1@email.com",
        players=[db_player_1, db_player_2]
    )

    db_team_2 = Team(
        name="Team 2",
        tla="T2",
        shortName="Team2",
        areaName="Argentina",
        email="team2@email.com",
        players=[db_player_3]
    )

    db_team_3 = Team(
        name="Team 3",
        tla="T3",
        shortName="Team3",
        areaName="Argentina",
        email="team3@email.com",
        players=[db_player_4]
    )

    db_competition_1 = Competition(
        name="Santex League",
        code='SL',
        areaName="Argentina",
        teams=[db_team_1, db_team_3]
    )

    db_competition_2 = Competition(
        name="Test League",
        code='TL',
        areaName="Argentina",
        teams=[db_team_2]
    )

    test_db.add_all([
        db_competition_1, db_competition_2,
        db_team_1, db_team_2,
        db_player_1, db_player_2, db_player_3
    ])

    test_db.commit()
