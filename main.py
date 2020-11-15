from flask import Flask, render_template, request, session, url_for, redirect, jsonify,g
from flask.views import MethodView
import sqlite3,pickle
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalch import (Table, Column, Integer, String)
  
app = Flask(__name__)
  
engine = create_engine('sqlite:///sample.sqlite3')
Base = declarative_base()
  
# get Database Object.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('sample.sqlite3')
        return g.db
  
# close Database Object.
def close_db(e=None):
    db = g.pop('db', None)
  
    if db is not None:
        db.close()
  
#model class
class Mydata(Base):
    __tablename__ = 'mydata'
  
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mail = Column(String(255))
    age = Column(Integer)
  
    # get Dict data
    def toDict(self):
        return{
            'id':int(self.id),
            'name':str(self.name),
            'mail':str(self.mail),
            'age':int(self.age)
        }
# get List data
def getByList(arr):
    res=[]
    for item in arr:
        res.append(item.toDict())
    return res
  
# get all mydata record
def getAll():
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = ses.query(Mydata).all()
    ses.close()
    return res
  
 
@app.route('/', methods=['GET'])
def index():
    return render_template('index1.html',\
        title='Sample code',)
@app.route('/search', methods=['GET'])
def index_search():
    return render_template('index2.html',\
        title='Sample code',)

# @app.route('/', methods=['GET'])
# def index():
#     mydata=[]:
#     db = get_db()
#     cur = db.execute("select * from mydata")
#     mydata = cur.frtchall()
#     return render_template('index1.htm',\
#         data=mydata)
#     return render_template('index.html',\
#         title='This is smaple of ORM',)
  
@app.route('/ajax', methods=['GET'])
def ajax():
    mydata = getAll()
    return jsonify(getByList(mydata));
  
@app.route('/form', methods=['post'])
def form():
    name = request.form.get('name')
    mail = request.form.get('mail')
    age = int(request.form.get('age'))
    mydata = Mydata(name=name, mail=mail, age=age)
    Session = sessionmaker(bind=engine)
    ses = Session()
    ses.add(mydata)
    ses.commit()
    ses.close()
    return'ok'
  
@app.route('/<id>', methods=['GET'])
def index_id(id):
    return render_template('index.html',\
        title='Sample of Update', id=id, \
        message='SQL',
        alert='Hello SQL')
 
@app.route('/ajax/<id>', methods=['GET'])
def ajax_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    ses.close()
    return jsonify(mydata.toDict());
 
@app.route('/form/<id>', methods=['post'])
def form_id(id):
    name = request.form.get('name')
    mail = request.form.get('mail')
    age = int(request.form.get('age'))
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    mydata.name = name
    mydata.mail = mail
    mydata.age = int(age)
    ses.add(mydata)
    ses.commit()
    ses.close()
    return 'ok'

@app.route('/delete/<id>', methods=['GET'])
def delete_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id ==id).one()
    ses.delete(mydata)
    ses.commit()
    ses.close()
    return "delete id =" + id

@app.route('/find', methods=['POST'])
def find():
    find = request.form.get('find')
    Session = sessionmaker(bind=engine)
    ses = Session()
    result = ses.query(Mydata).\
        filter(Mydata.name == find).all()
    ses.close()
    return jsonify(getByList(result));

 
if __name__ == '__main__':
    app.debug=True
    app.run()