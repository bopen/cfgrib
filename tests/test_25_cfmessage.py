
from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import numpy as np

from cfgrib import cfmessage

SAMPLE_DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'sample-data')
TEST_DATA = os.path.join(SAMPLE_DATA_FOLDER, 'era5-levels-members.grib')


def test_from_grib_date_time():
    message = {
        'dataDate': 20160706,
        'dataTime': 1944,
    }
    result = cfmessage.from_grib_date_time(message)

    assert result == 1467834240


def test_to_grib_date_time():
    message = {}
    datetime = np.datetime64('2001-10-11T01:01:00', 's')

    cfmessage.to_grib_date_time(message, datetime)

    assert message['dataDate'] == 20011011
    assert message['dataTime'] == 101


def test_from_grib_step():
    message = {
        'endStep': 1,
        'stepUnits': 1,
    }
    step_seconds = cfmessage.from_grib_step(message)

    assert step_seconds == 60 * 60


def test_to_grib_step():
    message = {}
    step = np.timedelta64(60 * 60, 's')

    cfmessage.to_grib_step(message, step=step, step_unit=1)

    assert message['endStep'] == 1
    assert message['stepUnits'] == 1


# def test_from_grib_pl_level():
#     message = {
#         'typeOfLevel': 'isobaricInhPa',
#         'topLevel': 1,
#     }
#

    from_grib_pl_level(message, level_key='topLevel')