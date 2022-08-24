# get users
curl http://127.0.0.1:5000/tasks

# post new user

# JSON
curl -d '{ "title": "Python API test", "notes": "Implementing a SQL Server database based Python API", "due_date": "2022-08-23" }' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/tasks -v

# WITH PARAMETERS
curl -d "userId=321&name=Vlad&city=Transilvania" -X POST http://localhost:5000/users

# put location
curl -d "userId=321&location=0007" -X PUT http://localhost:5000/users

# delete
curl -d "userId=321" -X DELETE http://localhost:5000/users
