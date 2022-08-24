from http.server import HTTPServer
from typing_extensions import Required
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import pymssql
from StudyTask import StudyTask, StudyTaskEncoder
from StudyTaskSql import StudyTaskSql
import json

app = Flask(__name__)
api = Api(app)

# api - use class to define
# local url: http://127.0.0.1:5000/tasks
class Tasks(Resource):
    _usersFile = "./csv/users.csv"      # keep until finish mssql implementations
    connDic = { 'server': 'localhost', 'user': 'sa', 'password': 'Cmaj7/#5', 'database': 'manjaro'}

    def get(self):
        conn = pymssql.connect(server = self.connDic['server'], user = self.connDic['user'], password = self.connDic['password'], database = self.connDic['database'])
        cursor = conn.cursor()
        cursor.execute('SELECT t.ID, t.TITLE, t.CREATION_DATE, t.UPDATE_DATE, t.NOTES, t.DUE_DATE FROM tasks t where t.REMOVED = 0 order by t.ID desc;')

        lst = []
        row = cursor.fetchone()

        while row:
            obj = StudyTask()
            obj.id = row[0]
            obj.title = row[1]
            obj.creation_date = row[2]
            obj.update_date = row[3]
            obj.notes = row[4]
            obj.due_date = row[5]
            lst.append(obj)
            row = cursor.fetchone()
        
        ret = json.dumps(lst, cls=StudyTaskEncoder)
        return {'data': ret}, 200

    # Insert new record.
    def post(self):
        # object parser bellow
        parser = reqparse.RequestParser()  # initialize

        # parse arguments from JSON
        parser.add_argument('title', required=True)
        parser.add_argument('notes', required=True)
        parser.add_argument('due_date', required=False)
        # parse argumentos to dictionary
        args = parser.parse_args()  
        dict = { 'title': args['title'], 'notes': args['notes'], 'due_date': args['due_date'], 'message': 'Request received'}
        studyTaskSql = StudyTaskSql(self.connDic, dict)
        studyTaskSql.Create()
        dict['message'] = 'Record inserted'
        return { 'data': dict }, 200

    # update one record
    # requires: id, title, notes, due_date
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('title', required=True)
        parser.add_argument('notes', required=True)
        parser.add_argument('due_date', required=True)
        # parse argumentos to dictionary
        args = parser.parse_args()  
        dict = { 'id': args['id'], 'title': args['title'], 'notes': args['notes'], 'due_date': args['due_date'], 'message': 'Request received' }
        studyTaskSql = StudyTaskSql(self.connDic, dict)
        studyTaskSql.update()
        dict['message'] = 'Updated successfully'
        return { 'data': dict }, 200

    # mark a record as removed
    # requires: id
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        args = parser.parse_args()
        dic = { 'id': args['id'] }
        studyTaskSql = StudyTaskSql(self.connDic, dic)
        studyTaskSql.remove()
        dic['message'] = 'Record removed successfully'
        return { 'data': dic }, 200



# '/tasks' is our entry point for Tasks
api.add_resource(Tasks, '/tasks')

# Control the app run and start
if __name__ == '__main__':
    app.run()  # run our Flask app
