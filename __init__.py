from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,DateTime,Boolean,Date,Float

from flask import render_template,request,redirect,url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

session = db.session


class Node_info(db.Model):
    __tablename__ = 'node_info'
    id = Column(Integer,primary_key=True)
    FrameID = Column(Integer)
    ProductName = Column(String(20))
    Producer = Column(String(50))
    Note = Column(String(100))
    IMEI = Column(String(20))
    Port = Column(Integer)
    UserName = Column(String(30))
    ProductSerialNumber = Column(String(15))
    SendTime = Column(DateTime)
    PhoneNumber = Column(String(11))
    SiginalStrengh  =Column(Integer)
    LightStrength = Column(Integer)
    Version = Column(String(10))
    ProductType = Column(String(20))
    Temperature = Column(Float)
    IMSI = Column(String(20))
    IP  = Column(String(20))
    TSINumber = Column(Integer)
    UserNote = Column(String(200))



import datetime

@app.route("/push",methods=["POST"])
def push():
    if(request.method=="POST"):
        new_element = Node_info(
            FrameID = int(request.form['FrameID']),
            ProductName =  request.form['ProductName'],
            Producer = request.form['Producer'],
            Note = request.form['Note'],
            IMEI = request.form['IMEI'],
            Port = int(request.form['Port']),
            UserName = request.form['UserName'],
            ProductSerialNumber = request.form['ProductSerialNumber'],
            SendTime = datetime.datetime.now(),
            PhoneNumber = request.form['PhoneNumber'],
            SiginalStrengh = int(request.form['SiginalStrengh']),
            LightStrength = int(request.form['LightStrength']),
            Version = request.form['Version'],
            ProductType = request.form['ProductType'],
            Temperature = float(request.form['Temperature']),
            IMSI = request.form['IMSI'],
            IP = request.form['IP'],
            TSINumber = int(request.form['TSINumber']),
            UserNote = request.form['UserNote']
        )
        print("One added.")
        session.add(new_element)
        session.commit()

        return "Fuck"

    return "Shit"

@app.route("/pull",methods=["GET","POST"])
def pull():
    if(request.method=="GET"):
        return render_template("nodes_info.html")
    else:

        node_list = []
        for IMEI in request['IMEI_list']:
            one = session.query(Node_info).filter(Node_info.IMEI==IMEI).first()
            node_list.append(one)

        return render_template("nodes_info.html",node_list=node_list)


if(__name__=="__main__"):
    db.create_all()
    app.run(host="0.0.0.0",port=5000)