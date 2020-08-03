import copy

from TwitterDataPoint import TwitterDataPoint
import pandas as pd
from datetime import datetime

from os import getcwd, path, chdir


class TwitterDataAgent:
    token_id = 0
    current_dp_index = 0
    terms_global_frequency = 0

    def __init__(self, count: int, epsilon=1e-7):
        self.epsilon = epsilon
        self.raw_data = None
        self.token_to_id = {}
        self.global_freq = {}
        self.count = count
        self.data_points = {}

        chdir('..')
        self.load_data(path.join(getcwd(), 'Data/data_cleaned1.pkl'), count=count)
        chdir('./Algo')

    def load_data(self, file_path: str, count: int) -> None:
        self.raw_data = pd.read_pickle(file_path).reset_index().head(count)

    def get_dp(self, dp: pd.DataFrame) -> TwitterDataPoint:
        tweet = dp['text'].values[0]

        # Extracting Data
        freq_dict = self.get_freq_dict(tweet)

        time_stamp = datetime.now()
        user_id = dp['user_id'].values[0]
        status_id = dp['status_id'].values[0]
        created_at = dp['created_at'].values[0]
        is_verified = dp['verified'].values[0]
        favourites_count = dp['favourites_count'].values[0]
        retweet_count = dp['retweet_count'].values[0]

        # Updating Current Date
        from KingAgent import KingAgent
        KingAgent.prev_data = copy.deepcopy(KingAgent.date)
        KingAgent.date = pd.to_datetime(created_at)

        return TwitterDataPoint(
            freq=freq_dict, time_stamp=time_stamp,
            user_id=user_id, status_id=status_id,
            created_at=created_at, is_verified=is_verified,
            favourites_count=favourites_count, retweet_count=retweet_count,
            index_in_df=TwitterDataAgent.current_dp_index - 1
        )

    def get_freq_dict(self, tweet: str) -> dict:
        tweet_tokens = tweet.split()

        freq_dict = {}
        for token in tweet_tokens:
            if token in self.token_to_id:
                if self.token_to_id[token] in freq_dict:
                    freq_dict[self.token_to_id[token]] += 1
                else:
                    freq_dict[self.token_to_id[token]] = 1
            else:
                self.token_to_id[token] = TwitterDataAgent.token_id
                TwitterDataAgent.token_id += 1
        return freq_dict

    def get_next_dp(self):
        if TwitterDataAgent.current_dp_index >= self.count:
            print('Finished')
            return None
        else:
            TwitterDataAgent.current_dp_index += 1
            dp = self.get_dp(self.raw_data.iloc[[TwitterDataAgent.current_dp_index - 1]])
            self.data_points[dp.dp_id] = dp
            return dp

    def has_next_dp(self):
        if TwitterDataAgent.current_dp_index >= self.count:
            return False
        else:
            return True