import pytest

import cfgrib
import cfgrib.xarray_store

import cdscommon


TEST_FILES = {
    'era5-land-reanalysis': [
        'reanalysis-era5-land',
        {
            'format': 'grib',
            'variable': '2m_dewpoint_temperature',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '01:00'],
        },
        197,
    ],
    'era5-land-monthly-means-monthly_averaged_reanalysis': [
        'reanalysis-era5-land-monthly-means',
        {
            'format': 'grib',
            'product_type': 'monthly_averaged_reanalysis',
            'variable': '2m_dewpoint_temperature',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        203,
    ],
    'era5-land-monthly-means-monthly_averaged_reanalysis_by_hour_of_day': [
        'reanalysis-era5-land-monthly-means',
        {
            'format': 'grib',
            'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
            'variable': '2m_dewpoint_temperature',
            'year': '2017',
            'month': '01',
            'time': ['00:00', '01:00'],
        },
        203,
    ],
}


@pytest.mark.parametrize('test_file', TEST_FILES.keys())
def test_Stream(test_file):
    dataset, request, key_count = TEST_FILES[test_file]
    path = cdscommon.ensure_data(dataset, request, name='cds-' + test_file + '-{uuid}.grib')

    stream = cfgrib.FileStream(path)
    leader = stream.first()
    assert len(leader) == key_count
    assert sum(1 for _ in stream) == leader['count']


@pytest.mark.parametrize('test_file', TEST_FILES.keys())
def test_Dataset(test_file):
    dataset, request, key_count = TEST_FILES[test_file]
    path = cdscommon.ensure_data(dataset, request, name='cds-' + test_file + '-{uuid}.grib')

    res = cfgrib.xarray_store.open_dataset(path)
    res.to_netcdf(path[:-5] + '.nc')

