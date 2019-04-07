import sys

sys.path.append('../../../dtest')

from dtest.dtest import Dtest

connectionConfig = {
    "host": "localhost",
    "username": "guest", # Can be set to None to bypass authentication
    "password": "guest", # Can be set to None to bypass authentication
    "exchange": "test.dtest",
    "exchange_type": "fanout"
}
metadata = {
    "description": "This is a test of the assertCondition",
    "topic": "test.dtest",
    "ruleSet": "Testing some random data",
    "dataSet": "random_data_set_123912731.csv"
}

dt = Dtest(connectionConfig, metadata)

dsQubert = [0,1]

dt.assertTrue(len(dsQubert) > 1, "len(dsQubert) > 1")

dt.finish()