import pytest

import cfgrib
import cfgrib.xarray_store

import cdscommon


TEST_FILES = {
    'cems-glofas-forecast-ensemble_perturbed_forecasts': [
        'cems-glofas-forecast',
        {
            'format': 'grib',
            'type': 'ensemble_perturbed_forecasts',
            'year': '2020',
            'month': '01',
            'day': '01',
            'step': ['24', '48'],
        },
        288,
    ],
    'cems-glofas-forecast-control_forecast': [
        'cems-glofas-forecast',
        {
            'format': 'grib',
            'type': 'control_forecast',
            'year': '2020',
            'month': '01',
            'day': '01',
            'step': ['24', '48'],
        },
        288,
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

