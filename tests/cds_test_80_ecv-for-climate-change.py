import pytest
import os
import zipfile

import cfgrib
import cfgrib.xarray_store

import cdscommon


TEST_FILES = {
    'cems-glofas-forecast-ensemble_perturbed_forecasts': [
        'ecv-for-climate-change',
        {
            'variable': 'surface_air_temperature',
            'product_type': 'anomaly',
            'time_aggregation': '1_month',
            'year': '2019',
            'month': '01',
            'origin': 'era5',
        },
        190
    ]
}


@pytest.mark.parametrize('test_file', TEST_FILES.keys())
def test_Stream(test_file):
    dataset, request, key_count = TEST_FILES[test_file]
    path_to_zip = cdscommon.ensure_data(
        dataset, request, name='cds-' + test_file + '-{uuid}.zip'
    )
    unzipped_dir = path_to_zip.replace('.zip', '')
    with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
        zip_ref.extractall(unzipped_dir)
        grib_file_names = zip_ref.namelist()
    paths = [
        os.path.join(unzipped_dir, file_name) for file_name in grib_file_names
    ]

    for path in paths:
        stream = cfgrib.FileStream(path)
        leader = stream.first()
        assert len(leader) == key_count
        assert sum(1 for _ in stream) == leader['count']


@pytest.mark.parametrize('test_file', TEST_FILES.keys())
def test_Dataset(test_file):
    dataset, request, key_count = TEST_FILES[test_file]
    path_to_zip = cdscommon.ensure_data(
        dataset, request, name='cds-' + test_file + '-{uuid}.zip'
    )
    unzipped_dir = path_to_zip.replace('.zip', '')
    with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
        zip_ref.extractall(unzipped_dir)
        grib_file_names = zip_ref.namelist()
    paths = [
        os.path.join(unzipped_dir, file_name) for file_name in grib_file_names
    ]

    for path in paths:
        res = cfgrib.xarray_store.open_dataset(path)
        res.to_netcdf(path[:-5] + '.nc')

