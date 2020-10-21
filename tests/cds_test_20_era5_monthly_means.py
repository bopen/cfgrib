import pytest

import cfgrib
import cfgrib.xarray_store

import cdscommon


TEST_FILES = {
    'era5-single-levels-monthly-means-monthly_averaged_reanalysis': [
        'reanalysis-era5-single-levels-monthly-means',
        {
            'format': 'grib',
            'product_type': 'monthly_averaged_reanalysis',
            'variable': '2m_temperature',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        190,
    ],
    'era5-single-levels-monthly-means-monthly_averaged_reanalysis_by_hour_of_day': [
        'reanalysis-era5-single-levels-monthly-means',
        {
            'format': 'grib',
            'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
            'variable': '2m_temperature',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        190,
    ],
    'era5-single-levels-monthly-means-monthly_averaged_ensemble_members': [
        'reanalysis-era5-single-levels-monthly-means',
        {
            'format': 'grib',
            'product_type': 'monthly_averaged_ensemble_members',
            'variable': '2m_temperature',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        192,
    ],
    'era5-single-levels-monthly-means-monthly_averaged_ensemble_members_by_hour_of_day': [
        'reanalysis-era5-single-levels-monthly-means',
        {
            'format': 'grib',
            'product_type': 'monthly_averaged_ensemble_members_by_hour_of_day',
            'variable': '2m_temperature',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        192,
    ],
    'era5-pressure-levels-monthly-means-monthly_averaged_reanalysis': [
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': 'divergence',
            'pressure_level': '1',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        190,
    ],
    'era5-pressure-levels-monthly-means-monthly_averaged_reanalysis_by_hour_of_day': [
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
            'variable': 'divergence',
            'pressure_level': '1',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        190,
    ],
    'era5-pressure-levels-monthly-means-monthly_averaged_ensemble_members': [
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_ensemble_members',
            'variable': 'divergence',
            'pressure_level': '1',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        192,
    ],
    'era5-pressure-levels-monthly-means-monthly_averaged_ensemble_members_by_hour_of_day': [
        'reanalysis-era5-pressure-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_ensemble_members_by_hour_of_day',
            'variable': 'divergence',
            'pressure_level': '1',
            'year': '2017',
            'month': ['01', '02'],
            'time': '00:00',
        },
        192,
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

