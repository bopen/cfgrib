import pytest

import cfgrib
import cfgrib.xarray_store

import cdscommon


TEST_FILES = {
    'uerra-europe-height-levels-reanalysis': [
        'reanalysis-uerra-europe-height-levels',
        {
            'format': 'grib',
            'variable': 'pressure',
            'height_level': '15_m',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '06:00'],
        },
        231,
    ],
    'uerra-europe-single-levels-reanalysis-mescan_surfex': [
        'reanalysis-uerra-europe-single-levels',
        {
            'format': 'grib',
            'origin': 'mescan_surfex',
            'variable': '10m_wind_direction',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '06:00'],
        },
        231,
    ],
    'uerra-europe-single-levels-reanalysis-uerra_harmonie': [
        'reanalysis-uerra-europe-single-levels',
        {
            'format': 'grib',
            'origin': 'uerra_harmonie',
            'variable': '10m_wind_direction',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '06:00'],
        },
        230,
    ],
    'uerra-europe-pressure-levels-reanalysis': [
        'reanalysis-uerra-europe-pressure-levels',
        {
            'format': 'grib',
            'variable': 'geopotential',
            'pressure_level': '10',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '06:00'],
        },
        230,
    ],
    'uerra-europe-soil-levels-reanalysis-mescan_surfex': [
        'reanalysis-uerra-europe-soil-levels',
        {
            'format': 'grib',
            'origin': 'mescan_surfex',
            'variable': 'volumetric_transpiration_stress_onset',
            'soil_level': '1',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '06:00'],
        },
        230,
    ],
    'uerra-europe-soil-levels-reanalysis-uerra_harmonie': [
        'reanalysis-uerra-europe-soil-levels',
        {
            'format': 'grib',
            'origin': 'uerra_harmonie',
            'variable': 'soil_temperature',
            'soil_level': '1',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': ['00:00', '06:00'],
        },
        231,
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

