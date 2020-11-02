import pytest

import cfgrib

import cdscommon


TEST_FILES = {
    'seasonal-original-single-levels-cmcc': [
        'seasonal-original-single-levels',
        {
            'originating_centre': 'cmcc',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'year': '2019',
            'month': ['04', '05'],
            'day': '01',
            'leadtime_hour': ['24', '48'],
            'format': 'grib',
        },
        193,
    ],
    'seasonal-original-pressure-levels-cmcc': [
        'seasonal-original-pressure-levels',
        {
            'originating_centre': 'cmcc',
            'variable': 'temperature',
            'pressure_level': ['500', '850'],
            'year': '2019',
            'month': ['04', '05'],
            'day': '01',
            'leadtime_hour': ['24', '48'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        193,
    ],
    'seasonal-postprocessed-single-levels-cmcc': [
        'seasonal-postprocessed-single-levels',
        {
            'originating_centre': 'cmcc',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours_anomaly',
            'product_type': 'ensemble_mean',
            'year': '2019',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        212,
    ],
    'seasonal-postprocessed-pressure-levels-cmcc': [
        'seasonal-postprocessed-pressure-levels',
        {
            'originating_centre': 'cmcc',
            'variable': 'temperature_anomaly',
            'product_type': 'ensemble_mean',
            'pressure_level': ['500', '850'],
            'year': '2019',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        212,
    ],
    'seasonal-monthly-single-levels-ensemble_mean-cmcc': [
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'cmcc',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'product_type': 'ensemble_mean',
            'year': '2019',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        212,
    ],
    'seasonal-monthly-pressure-levels-ensemble_mean-cmcc': [
        'seasonal-monthly-pressure-levels',
        {
            'originating_centre': 'cmcc',
            'variable': 'temperature',
            'product_type': 'ensemble_mean',
            'pressure_level': ['500', '850'],
            'year': '2019',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        212,
    ],
}


@pytest.mark.parametrize('test_file', TEST_FILES.keys())
def test_reanalysis_Stream(test_file):
    dataset, request, key_count = TEST_FILES[test_file]
    path = cdscommon.ensure_data(dataset, request, name='cds-' + test_file + '-{uuid}.grib')

    stream = cfgrib.FileStream(path)
    leader = stream.first()
    assert len(leader) == key_count
    assert sum(1 for _ in stream) == leader['count']


@pytest.mark.parametrize('test_file', TEST_FILES.keys())
def test_reanalysis_Dataset(test_file):
    dataset, request, key_count = TEST_FILES[test_file]
    path = cdscommon.ensure_data(dataset, request, name='cds-' + test_file + '-{uuid}.grib')

    res = cfgrib.xarray_store.open_dataset(path)
    res.to_netcdf(path[:-5] + '.nc')
