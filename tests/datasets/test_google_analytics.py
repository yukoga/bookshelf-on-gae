# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pytest
from recommend.datasets.google_analytics import GoogleAnalytics
from warnings import warn


@pytest.fixture
def data():
    try:
        params = {}
        params['api_name'] = 'analyticsreporting'
        params['api_version'] = 'v4'
        params['scope'] = 'https://www.googleapis.com/auth/analytics.readonly'
        params['service_account_email'] = \
            'yukoga-analytics-api@gcp-jp.iam.gserviceaccount.com'
        params['key_file_location'] = './gcp-jp.p12'
        ga = GoogleAnalytics(params=params)
        query_params = {
            'ids': 'ga:114540399',
            'start_date': '2016-01-01',
            'end_date': '2016-07-20',
            'dimensions': 'ga:date,ga:hour',
            'metrics': 'ga:sessions,ga:pageviews'
        }
        ga.fetch_data(query_params)
        return ga
    except TypeError:
        warn('Failed to fetch Google Analytics data. {}'
             .format(TypeError))


def test_googleanalytics_instantiation(data):
    # check if data type is correct.
    assert isinstance(data, GoogleAnalytics)
    assert isinstance(data.total, pd.DataFrame)
#    assert isinstance(data.features, pd.DataFrame)
#    assert isinstance(data.target, pd.Series)


def test_googleanalytics_data_shape(data):
    num_columns = 4  # ['ga:date', 'ga:hour', 'ga:sessions', 'ga:pageviews']
    num_records = 1000  # should have 1000 records for test dataset.
    assert len(data.total) == num_records
    assert len(data.total.T) == num_columns


def test_googleanalytics_data_summary(data):
    expected_summary_df = pd.DataFrame([[1000, 1000, 1000, 1000],
                                       [98, 24, 10, 14],
                                       ['20160223', '16', '1', '1'],
                                       [20, 66, 577, 483]])
    expected_summary_df.index = ['count', 'unique', 'top', 'freq']
    expected_summary_df.columns = ['date', 'hour', 'sessions', 'pageviews']

    assert data.total.describe().equals(expected_summary_df)
