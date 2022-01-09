from flask import Flask, render_template, request
from werkzeug.utils import redirect
app = Flask(__name__) 

@app.route('/') 
def hello(): 
    return 'Hello, World!'  

# Flask class's instance = our WSGI application
app = Flask(__name__)  

@app.route('/')
def index():
  return render_template('index.html')

@app.route("/<username>")
def user(username):
  return render_template("index.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word: 
    word = word.lower()
  else: 
    # redirect(url_for("index", msg="please enter a job"))
    return redirect("/")
  return render_template("report.html", searchingBy=word)

if __name__== "__main__" :
    app.run(debug=True)

