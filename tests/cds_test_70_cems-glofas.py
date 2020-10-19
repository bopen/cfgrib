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


@pytest.mark.skip()
def test_large_Dataset():
    dataset, request, key_count = TEST_FILES['era5-pressure-levels-ensemble_members']
    # make the request large
    request['day'] = list(range(1, 32))
    request['time'] = list(['%02d:00' % h for h in range(0, 24, 3)])
    path = cdscommon.ensure_data(dataset, request, name='cds-' + dataset + '-LARGE-{uuid}.grib')

    res = cfgrib.xarray_store.open_dataset(path)
    res.to_netcdf(path[:-5] + '.nc')
