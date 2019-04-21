The json file (test_definitions.json) contains the configuration of the data elements and the tests that need to be executed. 

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


## Requirements for the current test file

* Local installation of spark
* Postgres and table setup
* dtest package

## Execution 

* `python testaton.py /tests/test_definitions.json`


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

