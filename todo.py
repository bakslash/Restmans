import datetime
from flask import Flask, flash, redirect ,request ,render_template, url_for
import peewee as pw
import wtforms as wt
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from utils import slugify

DATABASE = {
    'name':'test.db',
    'engine':'peewee.SqliteDatabase',
}

DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)
db = database(app)

# Models
user = auth.get_user_model()

class Task(db.Model):
    task = pw.TextField()
    user = pw.ForeignKeyField(user)
    created = pw.DateTimeField(default=datetime.datetime.now)
    due = pw.DateField()


    #property
    def tags(self):
        return Tag.select().join(TaskTag).join(Task).where(Task.id == self.id)   
