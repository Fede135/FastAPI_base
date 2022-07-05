import datetime

from app.utils.constants import FOOTBALL_URL
from app.utils.football_api_proxy import Proxy
from app.utils.utils import format_date_of_birth_players, get_api_footbal_url


def test_proxy_singleton():
    proxy_1 = Proxy()
    proxy_2 = Proxy()
    assert proxy_1 == proxy_2
    assert proxy_1.client == proxy_2.client


def test_format_date_of_birth_players():
    date_api_v2 = "1987-12-31T02:26:44Z"
    date_api_v4 = "1987-12-31"
    expected = datetime.date(1987, 12, 31)
    result_v2 = format_date_of_birth_players(date_api_v2)
    result_v4 = format_date_of_birth_players(date_api_v4)
    assert expected == result_v2
    assert expected == result_v4


def test_get_api_football_url():
    url_v2 = get_api_footbal_url()
    url_v4 = get_api_footbal_url('v4')
    expected_v2 = FOOTBALL_URL.format('v2')
    expected_v4 = FOOTBALL_URL.format('v4')
    assert url_v2 == expected_v2
    assert url_v4 == expected_v4
