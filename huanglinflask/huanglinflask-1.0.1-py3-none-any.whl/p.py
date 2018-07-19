#encoding : utf-8

from flask import Flask ,url_for,redirect,render_template,session,request

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method== 'GET':

        return render_template('login.html')
    else:
        return render_template('regist.html')

@app.route('/regist/')
def regist():
    return render_template('regist.html')

@app.route('/logint/',methods=['get','POST'])
def  logint():
    if request.method=='POST':
        q=request.form.get('tel')
        p=request.form.get('password')
        print(q)
        print(p)

        return render_template('index.html')+q+'从v成本'+ p

@app.route('/search/',methods=['GET','POST'])
def search():
    if request.method=='POST':
        s= request.form.get('search')
        return s
    else:
        return 'sdfsdf'



if  __name__ =='__main__':

    app.run()