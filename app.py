# app.py
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response,jsonify
from flask_cors import CORS, cross_origin

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

# @app.route('/')
# def index():
#     return render_template('index.html')

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
            message = "<h1>User "+dataIn['username']+" has login !!!</h1>"
        return message
    except Exception as e:
        return str(e)#"<h1>Opps!! Something went wrong !!!</h1>"
    

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)