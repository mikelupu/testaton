from generate_sql import generate_uniqueness_sql, generate_fk_sql
from test_executor import run_in_db, run_in_spark

from pyspark.sql import SparkSession
from pyspark.sql import functions as sf

import pandas as pd
import sqlalchemy as sql

import argparse

import sys
sys.path.append('../../../dtest')
from dtest.dtest import Dtest

#Setup the data testing framework
connectionConfig = {
    "host": "localhost",
    "username": None,
    "password": None,
    "exchange": "test.dtest",
    "exchange_type": "fanout"
}
metadata = {
    "description": "Execution of the test_definition.json",
    "topic": "test.dtest",
    "ruleSet": "Test a couple of files and tables",
    "dataSet": "Plenty to test files"
}

dt = Dtest(connectionConfig, metadata)

class Connection:
    """An object to represent a connection to a dataset, e.g. JDBC string, file location, etc"""
    def __init__(self, connection_def):
        self.type = connection_def['type']
        if self.type == "JDBC connection":
            self.connection_string = connection_def['connection-string']

class Dataset:
    """An object that defines a dataset upon which operations will be conducted"""
    def __init__(self, connection_dict, dataset_definition):
        self.type = dataset_definition['type']
        self.connection = connection_dict[dataset_definition['connection']]
        self.location = dataset_definition['location']
        self.table_name = dataset_definition['table-name']
        self.setup(dataset_definition)

    def validate(self):
        """Validates whether the dataset exists and can be accessed"""
        #TODO create code to validate
        pass

    def setup(self, dataset_definition):
        """Setups up the dataset into a table if it needs to be setup"""
        if self.type == 'db-query':
                #TODO this might need a refactor
                viewSql = "create or replace view " + self.table_name + " as " + \
                            dataset_definition['query'] 
                engine = sql.create_engine(self.connection.connection_string)
                engine.execute(viewSql)
     
        if self.type[0:4] == 'file':
            spark = SparkSession \
                .builder \
                .master("local") \
                .appName("TestingApp") \
                .getOrCreate()
            if self.type == 'file-parquet':
                df = spark.read.parquet(self.location)
                df.createOrReplaceTempView(self.table_name)                 
            if self.type == 'file-csv':
                df = spark.read.format("csv").option("header", "true").load(self.location)
                df.createOrReplaceTempView(self.table_name)

    def destroy(self):
        """Destroys temporary created datasets that where setup"""
        #TODO implement


def get_execution_environment(dataset):
    if dataset.type[0:2] == 'db':
        return {'type': 'db', 'connection' : dataset.connection}
    if dataset.type[0:4] == 'file':
        return {'type': 'file', 'connection' : dataset.location}

class Test:
    def __init__(self, dataset_dict, tests_definition):
        self.description = tests_definition['description']
        self.type = tests_definition['test_type']
        self.definition = tests_definition

        if self.type == 'unique':
            self.dataset = [dataset_dict[tests_definition['table']]]
            self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_uniqueness_sql(dataset_dict, tests_definition) 

        if self.type == 'foreign_key':
            self.dataset = [dataset_dict[tests_definition['parent_table']],
                            dataset_dict[tests_definition['child_table']]]
            if len(set([get_execution_environment(d)['type'] for d in self.dataset])) > 1:
                print("Operation across multiple types of datasets not currently supported")
                exit(-1)
            else:
                self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_fk_sql(dataset_dict, tests_definition) 


    #Executes a test against a database
    def execute_db(self):
        print(self.sql)
        print(self.execution_env['connection'])
        return run_in_db(self.sql, self.execution_env['connection'].connection_string)

    #Execute a test in spark against a file
    def execute_file(self):
        return run_in_spark(self.sql)

    def execute(self):
        if self.execution_env['type'] == 'db':
            result = self.execute_db()
        if self.execution_env['type'] == 'file':
            result = self.execute_file()

        if self.type == 'unique':
            #TODO incorporate this with DTest
            if len(result) == 0:
                print("Test: " + self.description + ";    PASSED")
            else:
                print("Test: " + self.description + ";    FAILED")
            dt.assertTrue(len(result) == 0, self.description)

        if self.type == 'foreign_key':
            if result['result_count'][0] == 0:
                print("Test: " + self.description + ";  PASSED")
            else:
                print("Test: " + self.description + ";  FAILED")
            dt.assertTrue(result['result_count'][0] == 0, self.description)


def process_connections(connection_definition):
    connections = {}
    for k in connection_definition.keys():
        connections[k] = Connection(connection_definition[k])
    return connections

def process_datasets(connection_dict, dataset_definition):
    datasets = {}
    for d_key in dataset_definition.keys():
        datasets[d_key] = Dataset(connection_dict, dataset_definition[d_key]) 
    return datasets

def process_tests(dataset_dict, tests_definition):
    tests = {}
    for t_key in tests_definition.keys():
        tests[t_key] = Test(dataset_dict, tests_definition[t_key])
    return tests






#### MAIN RUN FILE ####
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test file')

    parser.add_argument('test_file', action='store', type=str, 
                        help='The JSON file defining the tests')

    args = parser.parse_args()

    import json 
    with open(args.test_file, 'r') as read_file:
        definition = json.load(read_file)

    connection_dict = process_connections(definition['connections'])
    datasets_dict = process_datasets(connection_dict, definition['data-definitions'])
    tests_dict = process_tests(datasets_dict, definition['tests'])

    for t in tests_dict:
        print(tests_dict[t].sql)
        tests_dict[t].execute()

    print(connection_dict)
    print(datasets_dict)
    print(tests_dict)

    #TODO this is breaking the call
    #dt.finish()