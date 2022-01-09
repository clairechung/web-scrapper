from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs
from exporter import save_to_file as save_to_file
app = Flask(__name__) 

# DB -should be outside of the route
db = {}    # 서버 시작하면 휘발되는 temp DB

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
    existingJobs = db.get(word)   # .get('nokey') returns None, but dic['nokey'] causes Error
    if existingJobs:      # if the word found in db, then
      jobs = existingJobs
    else:           # # if not found in db, then
      jobs = get_jobs(word)
      db[word] = jobs
  else: 
    # redirect(url_for("index", msg="please enter a job"))
    return redirect("/")
  return render_template(
    "report.html", 
    searchingBy=word, 
    resultNumber=len(jobs),
    jobs=jobs
    )

@app.route("/export")
def export():
  try: 
    word = request.args.get('word')
    if not word:
      raise Exception()   # means raise error -> go to except:   # or I may use ['key'] and get rid of raising Error
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    return send_file(f"{word}.csv", as_attachment=True)
  except:
    return redirect("/")


if __name__== "__main__" :
    app.run(debug=True)

