# app.py
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response,jsonify
from flask_cors import CORS, cross_origin

from script import runScript
import os

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



import time


class TwitterBot:
    
    def __init__(self,username, password):
        self.username=username
        self.password=password
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.bot=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    def login(self):
        bot=self.bot
        bot.get('https://twitter.com/login')
        # bot.switch_to.window(bot.window_handles[-1])
        time.sleep(3)
        email=bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        url=bot.current_url
        return url


@app.route('/api/getsample', methods=['POST'])
@cross_origin()
def getsample():
    try:
        dataIn= request.json
        message = ''
        if request.method == 'POST':
            ed=TwitterBot(dataIn['username'],dataIn['password'])
            # print((dataIn))
            res=ed.login()
            message = f"<h1>User "+dataIn['username']+" has access '{res}' !!!</h1>"
        return message
    except Exception as e:
        return str(e)#"<h1>Opps!! Something went wrong !!!</h1>"
@app.route('/script', methods = ['POST'])  
def login():
    keyWord=request.form['uname']
    ans = runScript(keyWord)
    return '<div>' +ans+ '</div>'

# A welcome message to test our server
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)