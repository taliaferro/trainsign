import pytest
import os
from .client import Open511Client


@pytest.fixture
def client():
    return Open511Client(api_key=os.getenv("TRAIN_SIGN_KEY"))


@pytest.mark.vcr()
def test_stop_monitoring(client):
    assert client.stop_monitoring("SF")


@pytest.mark.vcr()
def test_vehicle_monitoring(client):
    assert client.vehicle_monitoring("SF")


@pytest.mark.vcr()
def test_operators(client):
    assert client.operators()


@pytest.mark.vcr()
def test_lines(client):
    assert client.lines("SF")


@pytest.mark.vcr()
def test_stops(client):
    assert client.stops("SF")


@pytest.mark.vcr()
def test_stop_places(client):
    assert client.stop_places("SF")


@pytest.mark.vcr()
def test_patterns(client):
    assert client.patterns("SF", "KT")


@pytest.mark.vcr()
def test_timetable(client):
    assert client.timetable("SF", "KT")


@pytest.mark.vcr()
def test_stop_timetable(client):
    # I don't know how this endpoint works
    # it won't accept any of the values I've tried for monitoring ref
    assert client.stop_timetable("SF", "14148")


@pytest.mark.vcr()
def test_holidays(client):
    assert client.holidays("SF")
