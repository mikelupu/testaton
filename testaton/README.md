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


## Example execution 

* `python tests_processor.py ./tests/test_definitions.json`


## TODO

- [x] add Dtest integration to the suite
- [ ] add a score function test against two variables from two data sets
- [ ] filter : a number is out of range (e.g. mileage < 0)
- [ ] count of yesterday's record > today + 10%
- [ ] count of null fields > amount
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