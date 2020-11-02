import pytest

import cfgrib

import cdscommon


TEST_FILES = {
    'seasonal-original-single-levels-ncep': [
        'seasonal-original-single-levels',
        {
            'originating_centre': 'ncep',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'year': '2020',
            'month': ['04', '05'],
            'day': '01',
            'leadtime_hour': ['24', '48'],
            'format': 'grib',
        },
        192,
    ],
    'seasonal-original-pressure-levels-ncep': [
        'seasonal-original-pressure-levels',
        {
            'originating_centre': 'ncep',
            'variable': 'temperature',
            'pressure_level': ['500', '850'],
            'year': '2020',
            'month': ['04', '05'],
            'day': '01',
            'leadtime_hour': ['24', '48'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        192,
    ],
    'seasonal-postprocessed-single-levels-ncep': [
        'seasonal-postprocessed-single-levels',
        {
            'originating_centre': 'ncep',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours_anomaly',
            'product_type': 'ensemble_mean',
            'year': '2020',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        211,
    ],
    'seasonal-postprocessed-pressure-levels-ncep': [
        'seasonal-postprocessed-pressure-levels',
        {
            'originating_centre': 'ncep',
            'variable': 'temperature_anomaly',
            'product_type': 'ensemble_mean',
            'pressure_level': ['500', '850'],
            'year': '2020',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        211,
    ],
    'seasonal-monthly-single-levels-ensemble_mean-ncep': [
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'ncep',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'product_type': 'ensemble_mean',
            'year': '2020',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        211,
    ],
    'seasonal-monthly-pressure-levels-ensemble_mean-ncep': [
        'seasonal-monthly-pressure-levels',
        {
            'originating_centre': 'meteo_france',
            'variable': 'temperature',
            'product_type': 'ensemble_mean',
            'pressure_level': ['500', '850'],
            'year': '2020',
            'month': ['04', '05'],
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        211,
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
