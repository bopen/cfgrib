import pytest

import cfgrib
import cfgrib.xarray_store

import cdscommon


TEST_FILES = {
    'efas-forecast-control_forecast-surface_level': [
        'efas-forecast',
        {
            'format': 'grib',
            'origin': 'ecmwf',
            'type': 'control_forecast',
            'variable': 'river_discharge_in_the_last_24_hours',
            'model_levels': 'surface_level',
            'year': '2018',
            'month': '10',
            'day': '11',
            'time': '00:00',
            'step': ['24', '48'],
        },
        271,
    ],
    'efas-forecast-ensemble_perturbed_forecasts-surface_level': [
        'efas-forecast',
        {
            'origin': 'ecmwf',
            'type': 'ensemble_perturbed_forecasts',
            'variable': 'river_discharge_in_the_last_24_hours',
            'model_levels': 'surface_level',
            'year': '2018',
            'month': '10',
            'day': '11',
            'time': '00:00',
            'step': ['24', '48'],
            'format': 'grib',
        },
        271,
    ],
    'efas-forecast-high_resolution_forecast-surface_level': [
        'efas-forecast',
        {
            'origin': 'ecmwf',
            'type': 'high_resolution_forecast',
            'variable': 'river_discharge_in_the_last_6_hours',
            'model_levels': 'surface_level',
            'year': '2018',
            'month': '10',
            'day': '11',
            'time': '00:00',
            'step': ['24', '48'],
            'format': 'grib',
        },
        268,
    ],
    'efas-forecast-control_forecast-soil_levels': [
        'efas-forecast',
        {
            'origin': 'ecmwf',
            'type': 'control_forecast',
            'variable': 'soil_depth',
            'model_levels': 'soil_levels',
            'year': '2019',
            'month': '01',
            'day': '30',
            'time': '00:00',
            'step': ['0', '24'],
            'format': 'grib',
            'soil_level': '1',
        },
        256,
    ],
    'efas-historical-version_4_0-surface_level': [
        'efas-historical',
        {
            'format': 'grib',
            'simulation_version': 'version_4_0',
            'variable': 'snow_depth_water_equivalent',
            'model_levels': 'surface_level',
            'hyear': '2017',
            'hmonth': 'january',
            'hday': ['01', '02'],
            'time': '06:00',
        },
        255,
    ],
    'efas-historical-version_3_5-surface_level': [
        'efas-historical',
        {
            'format': 'grib',
            'simulation_version': 'version_3_5',
            'variable': 'river_discharge',
            'model_levels': 'surface_level',
            'hyear': '2017',
            'hmonth': 'january',
            'hday': ['01', '02'],
            'time': '06:00'
        },
        269,
    ],
    'efas-historical-version_3_0-surface_level': [
        'efas-historical',
        {
            'format': 'grib',
            'simulation_version': 'version_3_0',
            'variable': 'river_discharge',
            'model_levels': 'surface_level',
            'hyear': '2017',
            'hmonth': 'january',
            'hday': ['01', '02'],
            'time': '06:00'
        },
        268,
    ],
    'efas-historical-version_2_0-surface_level': [
        'efas-historical',
        {
            'format': 'grib',
            'simulation_version': 'version_2_0',
            'variable': 'river_discharge',
            'model_levels': 'surface_level',
            'hyear': '2017',
            'hmonth': 'january',
            'hday': ['01', '02'],
            'time': '06:00'
        },
        268,
    ],
    'efas-historical-version_4_0-soil_level': [
        'efas-historical',
        {
            'format': 'grib',
            'simulation_version': 'version_4_0',
            'variable': 'soil_depth',
            'model_levels': 'soil_levels',
            'hyear': '2017',
            'hmonth': 'january',
            'hday': ['01', '02'],
            'time': '06:00',
            'soil_level': '1',
        },
        254,
    ],
    'efas-historical-version_3_5-soil_level': [
        'efas-historical',
        {
            'format': 'grib',
            'simulation_version': 'version_3_5',
            'variable': 'soil_depth',
            'model_levels': 'soil_levels',
            'hyear': '2017',
            'hmonth': 'january',
            'hday': ['01', '02'],
            'soil_level': '1',
            'time': '06:00'
        },
        254,
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
