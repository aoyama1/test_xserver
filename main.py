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


#####TOPページ#########################################
@app.route('/', methods=['GET'])
def index():
    return render_template('index_top.html',\
        title="実施したい項目を選んでください"
        )


##### 新規作成 #######################################
@app.route('/create', methods=['GET'])
def create():
    return render_template('index_create.html',\
        title='新規作成',)
 
@app.route('/create/ajax', methods=['GET'])
def ajax_create():
    mydata = getAll()
    return jsonify(getByList(mydata));
 
@app.route('/create/form', methods=['post'])
def form_create():
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

###### 検索 ##########################################
@app.route('/find', methods=['POST'])
def find():
    find = request.form.get('find')
    Session = sessionmaker(bind=engine)
    ses = Session()
    result = ses.query(Mydata).\
        filter(Mydata.name == find).all()
    ses.close()
    return jsonify(getByList(result));

@app.route('/fi', methods=['GET'])
def fi():
    return render_template('index_find.html',\
        title='レコードの検索',)
   
@app.route('/fi/ajax', methods=['GET'])
def fi_ajax():
    mydata = getAll()
    return jsonify(getByList(mydata));
   
@app.route('/fi/form', methods=['post'])
def fi_form():
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
   
@app.route('/fi/<id>', methods=['GET'])
def fi_index_id(id):
    return render_template('index.html',\
        title='Sample of Update', id=id, \
        message='SQL',
        alert='Hello SQL')
  
@app.route('/fi/ajax/<id>', methods=['GET'])
def fi_ajax_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    ses.close()
    return jsonify(mydata.toDict());
  
@app.route('/fi/form/<id>', methods=['post'])
def fi_form_id(id):
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
###################################################

#######更新########################################

@app.route('/update', methods=['GET'])
def update_sel():
    return render_template('index_update_sel.html',\
        title='レコードの更新',)

@app.route('/up/ajax', methods=['GET'])
def up_ajax():
    mydata = getAll()
    return jsonify(getByList(mydata));
  
@app.route('/up/form', methods=['post'])
def up_form():
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
  
@app.route('/up/<id>', methods=['GET'])
def up_index_id(id):
    return render_template('index_update.html',\
        title='レコードIDの更新', id=id, \
        alert='Hello SQL')
 
@app.route('/up/ajax/<id>', methods=['GET'])
def up_ajax_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    ses.close()
    return jsonify(mydata.toDict());
 
@app.route('/up/form/<id>', methods=['post'])
def up_form_id(id):
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
###########削除##################################################


@app.route('/delete', methods=['GET'])
def delete_sel():
    return render_template('index_delete_sel.html',\
        title='レコードの削除',)

@app.route('/del/<id>', methods=['GET'])
def del_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id ==id).one()
    ses.delete(mydata)
    ses.commit()
    ses.close()
    return "delete id =" + id

################################################################

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

if __name__ == '__main__':
    app.debug=True
    app.run()