from core.models import IotDeviceData
from core.forms import status_as_str, ROTOR_SPEED, SLACK, ROOT_THRESHOLD, EQ, GTE, LTE


def get_filtered_data(cleaned_data: dict):
    filters = {}

    # Apply filter for status if any
    if int(cleaned_data['status']) > 0:
        filters['status'] = status = status_as_str(cleaned_data['status'])

    # Get compare filter for Operating Parameters if any
    comp = ''
    if int(cleaned_data['operating_param']) > 0:
        if int(cleaned_data['compare']) == EQ:
            comp = ''
        elif int(cleaned_data['compare']) == GTE:
            comp = '__gte'
        elif int(cleaned_data['compare']) == LTE:
            comp = '__lte'
        else:
            comp = ''

    # Apply filter for Operating Parameters if any
    key_str = ''
    if int(cleaned_data['operating_param']) == ROTOR_SPEED:
        key_str = 'rotor_speed' + comp
    elif int(cleaned_data['operating_param']) == SLACK:
        key_str = 'slack' + comp
    elif int(cleaned_data['operating_param']) == ROOT_THRESHOLD:
        key_str = 'root_threshold' + comp
    if key_str:
        filters[key_str] = int(cleaned_data['value'])

    data = IotDeviceData.objects.filter(**filters)
    return data
