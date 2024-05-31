from parse import *
import requests as rq

def test_get_id_from_kp():
    assert int(get_id_from_kp("Трое в лодке")) == 94973

def test_get_main_channels():
    ch = get_main_channels()
    assert len(ch) == 20

def test_get_url_from_kp():
    assert get_url_from_kp("Маша и Медведь") == "/film/478491"

def test_get_rating_from_kp():
    kp, imdb = get_rating("Трое в лодке")
    assert kp is not None
    assert imdb is not None
    kp, imdb = get_rating("asdfyhkio")
    assert kp is None
    assert imdb is None