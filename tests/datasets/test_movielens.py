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


@pytest.fixture
def data():
    try:
        ml = MovieLens()
        ml.fetch_data()
        return ml
    except:
        raise Exception('Failed to fetch movielens data.')


def test_movielens_shape_consistency(data):
    # check if data type is correct.
    assert isinstance(data, MovieLens)
    assert isinstance(data.features, pd.DataFrame)
    assert isinstance(data.target, pd.Series)


def test_movielens_length_consistency(data):
    # check if data volume is correct.
    assert len(data.features) == NUM_RECORDS
    assert len(data.target) == NUM_RECORDS
    assert len(data.features.T) == NUM_FEATURES


def test_movielens_info_check(data):
    info = pd.DataFrame.from_csv(
        path='http://files.grouplens.org/datasets/movielens/ml-100k/u.info',
        sep=' ',
        header=None,
        index_col=None)
    info.columns = ['num_records', 'dataset']
    __NUM_RECORDS = info['num_records'][2]
    assert len(data.features) == NUM_RECORDS
    assert len(data.target) == NUM_RECORDS
    assert len(data.features.T) == NUM_FEATURES


def test_movielens_data_summary(data):
    assert 0
