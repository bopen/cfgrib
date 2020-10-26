import pytest

import cfgrib

import cdscommon


TEST_FILES = {
    'seasonal-original-single-levels-jma': [
        'seasonal-original-single-levels',
        {
            'originating_centre': 'jma',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'year': '2020',
            'month': '09',
            'day': ['03', '08'],
            'leadtime_hour': ['24', '48'],
            'format': 'grib',
        },
        192,
    ],
    'seasonal-original-pressure-levels-jma': [
        'seasonal-original-pressure-levels',
        {
            'originating_centre': 'jma',
            'variable': 'temperature',
            'pressure_level': ['500', '850'],
            'year': '2020',
            'month': '09',
            'day': ['03', '08'],
            'leadtime_hour': ['24', '48'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        192,
    ],
    'seasonal-postprocessed-single-levels-jma': [
        'seasonal-postprocessed-single-levels',
        {
            'originating_centre': 'jma',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours_anomaly',
            'product_type': 'monthly_mean',
            'year': '2020',
            'month': '10',
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        213,
    ],
    'seasonal-monthly-single-levels-monthly_mean-jma': [
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'jma',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'product_type': 'monthly_mean',
            'year': '2020',
            'month': '10',
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        213,
    ],
    'seasonal-monthly-single-levels-ensemble_mean-jma': [
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'jma',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'product_type': 'ensemble_mean',
            'year': '2020',
            'month': '10',
            'leadtime_month': ['1', '2'],
            'grid': ['3', '3'],
            'format': 'grib',
        },
        211,
    ],
    'seasonal-monthly-single-levels-hindcast_climate_mean-jma': [
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'jma',
            'variable': 'maximum_2m_temperature_in_the_last_24_hours',
            'product_type': 'hindcast_climate_mean',
            'year': '2020',
            'month': '10',
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
