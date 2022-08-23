from http.server import HTTPServer
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import pymssql
from StudyTask import StudyTask, StudyTaskEncoder
import json

app = Flask(__name__)
api = Api(app)

# api - use class to define
class Tasks(Resource):
    _usersFile = "./csv/users.csv"      # keep until finish mssql implementations
    connDic = { 'server': 'localhost', 'user': 'sa', 'password': 'Cmaj7/#5', 'database': 'manjaro'}

    def get(self):
        conn = pymssql.connect(server = self.connDic['server'], user = self.connDic['user'], password = self.connDic['password'], database = self.connDic['database'])
        cursor = conn.cursor()
        cursor.execute('SELECT t.ID, t.TITLE, t.CREATION_DATE, t.UPDATE_DATE FROM tasks t where t.REMOVED = 0 order by t.ID desc;')

        lst = []
        row = cursor.fetchone()

        while row:
            obj = StudyTask()
            obj.id = row[0]
            obj.title = row[1]
            obj.creation_date = row[2]
            obj.update_date = row[3]
            lst.append(obj)
            row = cursor.fetchone()
        
        ret = json.dumps(lst, cls=StudyTaskEncoder)
        return {'data': ret}, 200

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()  # parse argumentos to dictionary

        # read our CSV
        data = pd.read_csv(self._usersFile)  # read the csv file

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 401
        else:
            # create new data frame containing new values
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [[]]
            })

            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            # save back to CSV
            data.to_csv('./csv/users.csv', index=False)
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        data = pd.read_csv(self._usersFile)

        if args['userId'] in list(data['userId']):
            # evaluate string of lists to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )

            data[data['userId'] == args['userId']].delete()

            # update users location
            user_data['locations'] = user_data['locations'].values[0].append(
                args['location'])

            # save back to CSV
            data.to_csv(self._usersFile, index=False)

            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise user does not exist
            return {
                'message': f"'{ args['userId'] }' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        args = parser.parse_args()

        data = pd.read_csv(self._usersFile)

        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]

            # save back to CSV
            data.to_csv(self._usersFile, index=False)

            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            return {
                'message': f"'{ args['userId'] }' user not found."
            }, 404


# '/tasks' is our entry point for Tasks
api.add_resource(Tasks, '/tasks')

# Control the app run and start
if __name__ == '__main__':
    app.run()  # run our Flask app
