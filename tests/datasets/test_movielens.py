# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pytest
from recommend.datasets.movielens import MovieLens
from warnings import warn


@pytest.fixture
def data():
    try:
        ml = MovieLens()
        ml.fetch_data()
        return ml
    except Exception:
        warn('Failed to fetch movielens data. {}'.format(Exception.message))


def test_movielens_instantiation(data):
    # check if data type is correct.
    assert isinstance(data, MovieLens)
    assert isinstance(data.features, pd.DataFrame)
    assert isinstance(data.target, pd.Series)


def test_movielens_data_shape(data):
    info = pd.DataFrame.from_csv(
        path='http://files.grouplens.org/datasets/movielens/ml-100k/u.info',
        sep=' ',
        header=None,
        index_col=None)
    __ratings = pd.DataFrame.from_csv(
        path='http://files.grouplens.org/datasets/movielens/ml-100k/u.data',
        sep='\t',
        header=None,
        index_col=None)
    __user = pd.DataFrame.from_csv(
        path='http://files.grouplens.org/datasets/movielens/ml-100k/u.user',
        sep='|',
        header=None,
        index_col=None)
    __item = pd.DataFrame.from_csv(
        path='http://files.grouplens.org/datasets/movielens/ml-100k/u.item',
        sep='|',
        header=None,
        index_col=None)
    info.columns = ['num_records', 'dataset']
    num_features = len(__ratings.columns) + \
        len(__user.columns) + len(__item.columns) - 3
    num_records = info['num_records'][2]
    assert len(data.features) == num_records
    assert len(data.target) == num_records
    assert len(data.features.T) == num_features


def test_movielens_data_summary(data):
    summary_mean = np.array([4.62484750e+02, 4.25530130e+02, 3.52986000e+00,
                             8.83528851e+08, 3.29698500e+01, 0.00000000e+00,
                             1.00000000e-04, 2.55890000e-01, 1.37530000e-01,
                             3.60500000e-02, 7.18200000e-02, 2.98320000e-01,
                             8.05500000e-02, 7.58000000e-03, 3.98950000e-01,
                             1.35200000e-02, 1.73300000e-02, 5.31700000e-02,
                             4.95400000e-02, 5.24500000e-02, 1.94610000e-01,
                             1.27300000e-01, 2.18720000e-01, 9.39800000e-02,
                             1.85400000e-02])
    summary_std = np.array([2.66614420e+02, 3.30798356e+02, 1.12567360e+00,
                            5.34385619e+06, 1.15626233e+01, 0.00000000e+00,
                            9.99954999e-03, 4.36362478e-01, 3.44407731e-01,
                            1.86415517e-01, 2.58190926e-01, 4.57522973e-01,
                            2.72144150e-01, 8.67330319e-02, 4.89684894e-01,
                            1.15487415e-01, 1.30498434e-01, 2.24373471e-01,
                            2.16993685e-01, 2.22933834e-01, 3.95902154e-01,
                            3.33310397e-01, 4.13380298e-01, 2.91802349e-01,
                            1.34894219e-01])

    summary_mean = np.round(summary_mean, -2)
    summary_std = np.round(summary_std, -2)
    summary_data = data.total.describe()
    summary_data_mean = np.round(summary_data[
        summary_data.index == 'mean'].fillna(0).values[0], -2)
    summary_data_std = np.round(summary_data[
        summary_data.index == 'std'].fillna(0).values[0], -2)

    assert all([mean in summary_mean for mean in summary_data_mean])
    assert all([std in summary_data_std for std in summary_std])
