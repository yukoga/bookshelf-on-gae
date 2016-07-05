# -*- coding: utf-8 -*-

import os
import pandas as pd
import pytest
import tempfile
from recommend.datasets.movielens import MovieLens
import path

DATASOURCE_URL = ""
NUM_RECORDS = 100000
NUM_FEATURES = 30
"""
NUM_FEATURES : number of meaningful features.
The output data which MovieLens class contains is
joined u.data and u.item, u.user by each ids.
Also the data includes only meaningful features as follows:
user id | item id | rating | timestamp |
release date | video release date |
Action | Adventure | Animation |
Children's | Comedy | Crime | Documentary | Drama | Fantasy |
Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
Thriller | War | Western |
age | gender | occupation | zip code.
"""


def _generate_tempdir_path(suffix="", prefix="tmp", dir=None):
    if dir is None:
        dir = tempfile.gettempdir()

    names = tempfile._get_candidate_names()

    for seq in range(100):
        name = names.next()
        path = os.path.join(dir, prefix + name + suffix)
        if not os.path.isdir(path):
            return path
        else:
            Exception('All temp dir name candidates exist. Try again.')


@pytest.fixture(scope='session')
def data_dir():
    return _generate_tempdir_path(prefix='recommend-of-')
#    return tempfile.mkdtemp(prefix="recommend-of-")


@pytest.fixture
def data(data_dir):
    try:
        ml = MovieLens()
        print(data_dir)
        data = ml.fetch_data()
        print(data['features'].head())
        print(data['target'].head())
        return data
    except IOError:
        raise Exception('Failed to fetch movielens data.')


def test_movielens_shape_consistency(data):
    # check if data type is correct.
    assert isinstance(data, dict)
    assert isinstance(data['features'], pd.DataFrame)
    assert isinstance(data['target'], pd.Series)


def test_movielens_length_consistency(data):
    # check if data volume is correct.
    assert len(data['features']) == NUM_RECORDS
    assert len(data['target']) == NUM_RECORDS
    assert len(data['features'].T) == NUM_FEATURES
