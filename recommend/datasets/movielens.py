# -*- coding: utf-8 -*-

import pandas as pd
from .abstract_dataset import AbstractDataset
try:
    from urllib2 import quote
except ImportError:
    from urllib.parse import quote

_BASE_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k/%s'

_DATA_STRUCTURE = {'ratings': {'filename': ['u.data', 'u1.base', 'u1.test', 'u2.base', 'u2.test', 'u3.base', 'u3.test', 'u4.base', 'u4.test', 'u5.base', 'u5.test', 'ua.base', 'ua.test', 'ub.base', 'ub.test'],
                               'sep': '\t',
                               'features': ['user_id', 'item_id', 'rating', 'timestamp']},
                   'users': {'filename': ['u.user'],
                             'sep': '|',
                             'features': ['user_id', 'age', 'gender', 'occupation', 'zip-code']},
                   'items': {'filename': ['u.item'],
                             'sep': '|',
                             'features': ['item_id', 'movie-title', 'release-date',
                                          'video-release-date', 'imdb-url', 'unknown',
                                          'action', 'adventure', 'animation',
                                          'children', 'comedy', 'crime',
                                          'documentary', 'drama', 'fantasy',
                                          'film-noir', 'horror', 'musical',
                                          'mystery', 'romance', 'sci-fi',
                                          'thriller', 'war', 'western']}
                   }


class MovieLens(AbstractDataset):

    def __init__(self):
        self.ratings = None
        self.users = None
        self.items = None
        self.features = None
        self.target = None
        self.total = None

    def fetch_data(self, query=None):
        self.ratings = self.fetch_table_data('ratings', 'u.data')
        self.users = self.fetch_table_data('users', 'u.user')
        self.items = self.fetch_table_data('items', 'u.item')
        features = self.__join_data(self.ratings, self.users, 'user_id')
        features = self.__join_data(features, self.items, 'item_id')
        self.total = features.copy()
        target = features['rating']
        del features['rating']
        self.features = features
        self.target = target

    def fetch_table_data(self, table_name=None, file_name=None):
        if table_name is None or isinstance(table_name, str) is False or len(table_name) is 0:
            raise ValueError('Table data is needed to be set.')
        else:
            __files = _DATA_STRUCTURE[table_name]['filename']
            if file_name in __files:
                __filename = __files[__files.index(file_name)]
            else:
                raise ValueError('Your specified file does not exist in the list. ')
            __sep = _DATA_STRUCTURE[table_name]['sep']
            __features = _DATA_STRUCTURE[table_name]['features']

        __url = _BASE_URL % quote(__filename)
        __df = pd.DataFrame.from_csv(
            __url, sep=__sep, header=None, index_col=None)
        __df.columns = __features

        return __df

    def __join_data(self, left_df=None, right_df=None, join_key=None):
        if all([isinstance(df, pd.DataFrame)
                for df in [left_df, right_df]]) is False:
            raise ValueError('The merge data must be instance of pandas DataFrame.')

        if join_key is None or isinstance(join_key, str) is False or len(join_key) is 0:
            raise ValueError('Join key must be needed.')

        if all([join_key in columns
                for columns in [left_df.columns, right_df.columns]]) is False:
            raise ValueError('Both left- and right-DataFrame should have common key to join.')

        merged = left_df.merge(right_df, left_on=join_key, right_on=join_key)
        return merged

    def __select_features(self, data=None, features=None):
        if features is None:
            features = data.columns

        return data[[column for column in features]]
