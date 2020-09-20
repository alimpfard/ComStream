class DataPoint:
    dp_id = 0

    def __init__(self,
                 freq: dict,
                 time_stamp,
                 created_at,
                 index_in_df):
        self.freq = freq
        self.created_at = created_at
        self.time_stamp = time_stamp
        self.index_in_df = index_in_df
        """
        the object that keeps the details of the dp
        :param freq: a dict of {token_id, frequency}
        :param time_stamp: the time the dp has come to system
        :param created_at: the time the dp was created at
        :param index_in_df: the index of the dp in the df
        :return: None
        """


class TwitterDataPoint(DataPoint):
    def __init__(self, freq: dict, time_stamp, user_id, status_id, created_at, is_verified, favourites_count,
                 retweet_count, index_in_df):
        """
        the child object of DataPoint
        :param freq: a dict of {token_id, frequency}
        :param time_stamp: the time the dp has come to system
        :param user_id: the id of the user
        :param status_id: the id of the tweet
        :param created_at: the time the dp was created at
        :param is_verified: Boolean
        :param favourites_count: the amount of likes
        :param retweet_count: the amount of retweets on this tweet
        :param index_in_df: the index of the dp in the df
        :return: None
        """
        super().__init__(freq, time_stamp, created_at, index_in_df)
        self.dp_id = DataPoint.dp_id
        DataPoint.dp_id += 1
        self.user_id = user_id
        self.status_id = status_id
        self.is_verified = is_verified
        self.favourites_count = favourites_count
        self.retweet_count = retweet_count
