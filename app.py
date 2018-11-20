# coding=utf-8
from flask import Flask,request,url_for,send_from_directory,render_template
from api import check as api_check
from json import dumps
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
@app.route("/paper/check",methods=["POST"])
def check():
    limit = int(request.form['limit'])
    file = request.files["file"]
    file.save("queries/a.jpg")
    result_file_data=api_check(limit)
    dict_result_data=[]
    divs=""
    model=" <div><span>{0}</span><img src={1}></div>"
    for result_file in result_file_data:
        # print(url_for(result_file[1],_external=True))
        divs=divs+model.format(int(result_file[0]*100)/100,"http://yun.chinadream.org:888/static/"+result_file[1][8:])
        #dict_result_data.append({"w":result_file[0],"url":"http://yun.chinadream.org:888/static/"+result_file[1][8:]})
   
    return html.format(divs)

@app.route("/paper/check_v2",methods=["POST"])
def check_v2():
    limit = int(request.form['limit'])
    file = request.files["file"]
    file.save("queries/a.jpg")
    result_file_data=api_check(limit)
    dict_result_data=[]
    for result_file in result_file_data:
        # print(url_for(result_file[1],_external=True))
        dict_result_data.append({"w":result_file[0],"url":"http://yun.chinadream.org:888/static/"+result_file[1][8:]})
   
    return dumps(dict_result_data)

@app.route("/paper/hello",methods=["POST"])
def hello():
    print(request.form) 
    return request.data.decode()+"------world"

@app.route("/paper/index",methods=["GET"])
def index():
    return render_template('index.html')


html='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
{0}
</body>
</html>'''



if __name__ == '__main__':
    app.run()
