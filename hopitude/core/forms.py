from django.forms import Form, ChoiceField, FloatField

MALFUNCTIONING = 1
STOPPED = 2
RUNNING = 3
STATUS_TYPE = ((0, ''),
               (MALFUNCTIONING, 'MALFUNCTIONING'),
               (STOPPED, 'STOPPED'),
               (RUNNING, 'RUNNING'),
               )

ROTOR_SPEED = 1
SLACK = 2
ROOT_THRESHOLD = 3
OPERATING_PARAM = ((0, ''),
                   (ROTOR_SPEED, 'ROTOR SPEED'),
                   (SLACK, 'SLACK'),
                   (ROOT_THRESHOLD, 'ROOT THRESHOLD'),
                   )

EQ = 1
GTE = 2
LTE = 3
COMPARE = ((0, ''),
           (EQ, '=='),
           (GTE, '>='),
           (LTE, '<='),
           )


class FilterForm(Form):
    status = ChoiceField(choices=STATUS_TYPE, required=False)
    operating_param = ChoiceField(choices=OPERATING_PARAM, required=False)
    compare = ChoiceField(choices=COMPARE, required=False)
    value = FloatField(required=False)


def status_as_str(value):
    for i in STATUS_TYPE:
        if int(value) == i[0]:
            return i[1]
    return None

