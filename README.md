The json file `example_config/configuration.json` contains an example configuration of Dtest, Spark, and the data elements and tests that need to be executed. 

There are 2 main types of connections:
* Database connections
* File connections (this will be subdivided into local and S3)

The data definition defines one of 3 things:
* A database table
* A file (csv or parquet)
* A database query

The tests define the tests that can be executed. Currently there are 2 types of tests implemented:
* Uniqueness - check for the uniqueness of a field
* Foreign Key constraint - check for a key not existing 

## Installation

`pip install testaton`

## Requirements

Local installation of spark if `spark-config:master` is set to `local`

## Execution 

`testaton configuration-file.json`

## Configuration
#### Dtest
See [Dtest](https://github.com/sjensen85/dtest) documentation.
`test-suite-metadata` is translated to the `metadata` argument
`message-broker-config` is translated to the `connectionConfig` argument

#### Spark
The configuration values for Spark are the master node and the application name. These translate to the corresponding arguments needed to build a SparkSession. More information can be found in the official [SparkSession documentation](https://spark.apache.org/docs/2.1.0/api/python/pyspark.sql.html?highlight=sparksession#pyspark.sql.SparkSession.Builder).

The `master` configuration variable sets the Spark master URL to connect to, such as “local” to run locally, “local[4]” to run locally with 4 cores, or “spark://ip-of-master:7077” to run on a Spark standalone cluster.

The `app-name` configuration variable sets a name for the application, which will be shown in the Spark web UI.

## TODO

- [ ] json configuration validator (syntax)
- [ ] validation of the existance of files, configurations, etc (semantics)
- [ ] add code tests
- [ ] remove username and password from test file
- [ ] filter : a number is out of range (e.g. mileage < 0)
- [ ] count of yesterday's record > today + 10%
- [ ] clean up code
- [ ] cross environment test execution (e.g. a table in a database and a file in parquet)
- [ ] create generic sql test
```
        "raw-query-test-example" : {
            "description" : "NOT IMPLEMENTED!! example of a raw sql test", 
            "test_type" : "custom_sql",
            "table" : "cinema-file",
            "sql_code" : "select count(1) error_cells from cinema where cinema_id < 1000",
            "validation" : "df['error_cells] < 100"
        }
```

## Done

- [x] add timing calculation to the execution of the test
- [x] count of null fields > amount 
- [x] complete Dtest integration to the suite (sending the message) 
- [x] add a score function test against two variables from two data sets

