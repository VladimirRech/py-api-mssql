import pymssql
from StudyTask import StudyTask

# Class for SQL Server object manipulation
class StudyTaskSql:
    'Class for SQL Server object manipulation'

    def __init__(self, dicConn, dicParams):
        self.DicConn = dicConn
        self.StudyTask = StudyTask()
        self.StudyTask.title = dicParams['title']
        self.StudyTask.notes = dicParams['notes']

        # Parsing due_date parameter properly
        if dicParams['due_date'] == '':
            self.due_date = None
        else:
            self.due_date = "'{0}'".format(dicParams['due_date'])

    # Insert record
    def Create(self):
        sql = "insert tasks (title, creation_date, update_date, notes, due_date) output INSERTED.ID values('{0}', getdate(), getdate(), '{1}', {2})".format(self.StudyTask.title, self.StudyTask.notes, self.due_date)
        print(sql)
        conn = pymssql.connect(server = self.DicConn['server'], user = self.DicConn['user'], password = self.DicConn['password'], database = self.DicConn['database'])
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()

        while row:
            print('Inserted ID: '.format(row[0]))
            row = cursor.fetchone()

        conn.commit()
        conn.close()