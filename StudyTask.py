from json import JSONEncoder
import datetime

#
# StudyTask
# Class to manipulate tasks
#
class StudyTask:
    'Class for tasks database objects'

    def __init__(self):
        self.id = 0
        self.creation_date = datetime.datetime.now()
        self.update_date = datetime.datetime.now()
        self.title = ''
        self.removed = False
        self.notes = ''
        self.due_date = datetime.datetime.now()

# JSON serializer to class
class StudyTaskEncoder(JSONEncoder):
    # Overwriting default serializer
    def default(self, obj):
        # for datetime serialization
        if isinstance(o, datetime.datetime):
            return obj.isoformat()

        return obj.__dict__