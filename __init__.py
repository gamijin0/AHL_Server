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
        attr_list_CN = ["端口","ID","生产厂家","IMEI号","产品名称","温度","IP地址","信号强度","手机号","IMSI号","光照强度","TSI触摸次数","产品类型","用户名称","发送时间","用户备注","版本号","产品序列号","帧ID","备注"]
        attr_list = ['Port', 'id', 'Producer', 'IMEI', 'ProductName', 'Temperature', 'IP', 'SiginalStrengh', 'PhoneNumber', 'IMSI', 'LightStrength', 'TSINumber', 'ProductType', 'UserName', 'SendTime', 'UserNote', 'Version', 'ProductSerialNumber', 'FrameID', 'Note']
        attr_dict = dict(zip(attr_list,attr_list_CN))
        node_list = []
        print(request.form)
        for IMEI in request.form['IMEI'].split():
            one = session.query(Node_info).filter(Node_info.IMEI==IMEI).first()
            node_list.append(one)

        return render_template("nodes_info.html",node_list=node_list,attr_dict = attr_dict)


if(__name__=="__main__"):
    db.create_all()
    app.run(host="0.0.0.0",port=5000)