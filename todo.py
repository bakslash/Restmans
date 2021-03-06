import datetime
from flask import Flask, flash, redirect ,request ,render_template, url_for
import peewee as pw
import wtforms as wt
from peewee import *
from flask_peewee.auth import Auth
from flask_peewee.db import Database
#from utils import slugify

DATABASE = {
    'name':'test.db',
    'engine':'peewee.SqliteDatabase',
}

DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)
db = Database(app)
auth = Auth(app, db)

# Models
user = auth.get_user_model()

class Task(db.Model):
    task = pw.TextField()
    user = pw.ForeignKeyField(user)
    created = pw.DateTimeField(default=datetime.datetime.now)
    due = pw.DateField()


    @property
    def tags(self):
        return Tag.select().join(TaskTag).join(Task).where(Task.id == self.id)   

class Tag(db.Model):
    tag = pw.TextField(unique=True)

class TaskTag(db.Model):
    task = pw.ForeignKeyField(Task)
    tag = pw.ForeignKeyField(Tag)

#forms
class Taskform(wt.Form):
    task = wt.TextField([wt.validators.Required()])
    tags = wt.TextField()
    due = wt.DateField

#Queries
def user_tasks():
    return Task.select().join(User).where(User.id == auth.get_logged_in_user())

def user_tagged_tasks(tag):
    tagged_tasks = TaskTag.select().join(Tag).where(Tag.tag == tag)
    tasks = Task.select().join(User).where(
        (User.id == auth.get_logged_in_user())&
        (Task.id << [t.task for t in tagged_tasks]))
    return tasks
