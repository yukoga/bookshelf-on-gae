# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pytest
from recommend.datasets.google_analytics import GoogleAnalytics
from warnings import warn


@pytest.fixture
def data():
    try:
        ga = GoogleAnalytics()
        ga.fetch_data()
        return ga
    except Exception:
        warn('Failed to fetch Google Analytics data. {}'.format(Exception.message))


def test_googleanalytics_instantiation(data):
    # check if data type is correct.
    assert isinstance(data, GoogleAnalytics)
    assert isinstance(data.total, pd.DataFrame)
    assert isinstance(data.features, pd.DataFrame)
    assert isinstance(data.target, pd.Series)


def test_googleanalytics_data_shape(data):
    num_columns = 4 # ['ga:date', 'ga:hour', 'ga:sessions', 'ga:pageviews']
    num_records = 1000 # should have 1000 records for test dataset.
    assert len(data.total) == num_records
    assert len(data.total.T) == num_columns


def test_googleanalytics_data_summary(data):
    expected_summry_df = pd.DataFrame([['1000','1000','1000','1000'],['98','24','10','14'],['20160223','16','1','1'],['20','66','577','483']])
    expected_summry_df.index = ['count', 'unique', 'top', 'freq']
    expected_summry_df.columns = ['date', 'hour', 'sessions', 'pageiews']

    assert data.total.describe() == expected_summry_df
