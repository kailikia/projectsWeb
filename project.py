from peewee import *

db = PostgresqlDatabase('company',user='postgres',host='localhost',password='Fuckyou31')
db.connect()
class Project(Model):
    id = AutoField()
    title = CharField()
    type = CharField()
    start_from = DateField()
    end_at = DateField()
    description = TextField()
    amount = DoubleField()
    status = IntegerField()

    class Meta:
        database = db # This model uses the "people.db" database.
        table_name = "projects"

Project.create_table(fail_silently=True)
# projectOne = Project(title= request.form['titleForm'],
#                      type="Internal",
#                      start_from = '2018-09-25',
#                      end_at = '2019-03-25',
#                      description = 'dinining hall for boarders',
#                      amount = 3540000,
#                      status = 1
#                      )
# projectOne.save()
#

#Get a record where the title equals Dining hall construction
# row1 = Project.get(Project.title == 'Dining hall construction')
#Print fields by using . operator getting field names from row1
# print(row1.title,row1.start_from)

#looping through all rows in the table
