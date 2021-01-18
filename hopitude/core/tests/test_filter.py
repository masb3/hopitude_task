import pytest

from core.models import IotDeviceData
from core.services.filter import get_filtered_data
from core.forms import MALFUNCTIONING, RUNNING, ROTOR_SPEED, SLACK, ROOT_THRESHOLD, EQ, GTE, LTE


db_data = [{'data_id': 1, 'timestamp': 1234567, 'status': 'RUNNING', 'rotor_speed': 500,
           'slack': 50.0, 'root_threshold': 100.0, 'asset_id': 1, 'asset_alias': 'Main Rotor Shaft',
            'parent_id': 1, 'parent_alias': 	'Counter Blades'},

           {'data_id': 2, 'timestamp': 1234567, 'status': 'MALFUNCTIONING', 'rotor_speed': 5000,
            'slack': 10.0, 'root_threshold': 10.0, 'asset_id': 1, 'asset_alias': 'Main Rotor Shaft',
            'parent_id': 1, 'parent_alias': 'Counter Blades'},

           {'data_id': 3, 'timestamp': 1234567, 'status': 'MALFUNCTIONING', 'rotor_speed': 400,
            'slack': 10.0, 'root_threshold': 10.0, 'asset_id': 1, 'asset_alias': 'Main Rotor Shaft',
            'parent_id': 1, 'parent_alias': 'Counter Blades'},
           ]


@pytest.mark.django_db
def test_filter_status(client):
    for data in db_data:
        IotDeviceData.objects.create(**data)
    user_filter = {'status': RUNNING, 'operating_param': 0}
    assert 1 == get_filtered_data(user_filter).count()


@pytest.mark.django_db
def test_filter_oper_param_rotor_speed(client):
    for data in db_data:
        IotDeviceData.objects.create(**data)
    user_filter = {'status': 0, 'operating_param': ROTOR_SPEED, 'compare': GTE, 'value': 500}
    assert 2 == get_filtered_data(user_filter).count()


@pytest.mark.django_db
def test_filter_oper_param_slack(client):
    for data in db_data:
        IotDeviceData.objects.create(**data)
    user_filter = {'status': 0, 'operating_param': SLACK, 'compare': LTE, 'value': 9}
    assert 0 == get_filtered_data(user_filter).count()


@pytest.mark.django_db
def test_filter_oper_param_root_threshold(client):
    for data in db_data:
        IotDeviceData.objects.create(**data)
    user_filter = {'status': 0, 'operating_param': ROOT_THRESHOLD, 'compare': EQ, 'value': 100}
    assert 1 == get_filtered_data(user_filter).count()


@pytest.mark.django_db
def test_filter_status_and_oper_param(client):
    for data in db_data:
        IotDeviceData.objects.create(**data)
    user_filter = {'status': MALFUNCTIONING, 'operating_param': SLACK, 'compare': EQ, 'value': 10}
    assert 2 == get_filtered_data(user_filter).count()
