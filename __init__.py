from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,DateTime,Boolean,Date,Float
import socket
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
            LightStrength = int(float(request.form['LightStrength'])),
            Version = request.form['Version'],
            ProductType = request.form['ProductType'],
            Temperature = float(request.form['Temperature']),
            IMSI = request.form['IMSI'],
            IP = get_host_ip(),
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
        series_temp_list = []
        series_light_list = []
        print(request.form)

        imei = request.form["IMEI"].split(";")
        imei_dict = dict(zip(imei,imei)) #去重


        for IMEI in imei_dict:
            items = session.query(Node_info).filter(Node_info.IMEI==IMEI).all()
            list.sort(items,key=lambda x:x.SendTime)

            utc = [int((item.SendTime-datetime.datetime(1970,1,1)).total_seconds()) for item in items]
            light_history = [item.LightStrength for  item in items]
            temperature_history = [item.Temperature for item in items]

            series_temp = {
                "name":"%s-温度" % IMEI,
                "data":list(zip(utc,light_history))
            }

            print(series_temp)

            series_temp_list.append(series_temp)
            series_light = {
                "name": "%s-光强" % IMEI,
                "data": list(zip(utc, temperature_history))
            }
            series_light_list.append(series_light)

            node_list.append(items[-1])

        series_list = series_light_list + series_temp_list

        return render_template("nodes_info.html",node_list=node_list,attr_dict = attr_dict,IMEIS = request.form["IMEI"],series_light_list = series_light_list,series_temp_list = series_temp_list, series_list=series_list)





def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

if(__name__=="__main__"):
    db.create_all()
    app.run(host="0.0.0.0",port=5000)
