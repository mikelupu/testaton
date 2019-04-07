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