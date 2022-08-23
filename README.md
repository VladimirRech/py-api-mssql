# py-api-mssql
Implementation of an API with Python and Microsoft SQL Server.
The intention is to be a template to start build any API with this products.
Starting trying to implement the code over Manjaro Linux. Why Manjaro? Because I like.

## Links
1. [Python SQL driver](https://docs.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver16)
1. [Python SQL Driver - pymssql](https://docs.microsoft.com/en-us/sql/connect/python/pymssql/python-sql-driver-pymssql?view=sql-server-ver16)
1. [POC with `pymssql`](https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-3-proof-of-concept-connecting-to-sql-using-pymssql?view=sql-server-ver16)
1. [Python references](https://www.tutorialspoint.com/python/python_environment.htm)
1. [Serialization to JSON 1](https://docs.python.org/3/library/json.html)
1. [Serialization to JSON 2](https://pynative.com/make-python-class-json-serializable/)
1. [Serialization to JSON - DATETIME](https://pynative.com/python-serialize-datetime-into-json/)
1. [Working with dates](https://www.geeksforgeeks.org/get-current-date-using-python/)

## Install `pymssql` on Manjaro Linux
```shell
# searching package
$  pamac search pymssql                                                                                     ✔ 
python-pymssql                                                                                             2.2.5-1  AUR 
    A simple database interface for Python that builds on top of FreeTDS to provide a Python DB-API
    (PEP-249) interface to Microsoft SQL Server
# INSTALL
$ sudo pamac install python-pymssql    
```