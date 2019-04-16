import pandas as pd
import sqlalchemy as sql
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as sf


import os
os.environ['SPARK_LOCAL_IP'] = "127.0.0.1"


def run_in_db(testSql, connection_string):
    print(connection_string)
    print(testSql)
    engine = sql.create_engine(connection_string)

    result = pd.read_sql_query(testSql, engine)
    return result


def run_in_spark(testSql):
    spark = SparkSession \
        .builder \
        .master("local") \
        .appName("TestingApp") \
        .getOrCreate()
    result = spark.sql(testSql)
    return result.toPandas()
