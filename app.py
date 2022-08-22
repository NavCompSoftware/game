from flask import *
from datetime import datetime,timedelta
import database_manager as db_man
import modes
import os

#Set up Flask app
app = Flask(__name__, static_url_path='/static')

#Start page
@app.route("/")

def index():
  db = db_man.init_SQL()
  db_man.confirm_tables(db)
  if db_man.scan_needed():
    try:
      db_man.maintain_db(db)
    except:
      pass
  db_man.save(db)
  return(render_template("home.html"))

#Page for players to join a game
@app.route("/join")

def join():
  return(render_template("join.html", message="Please enter your details to join a game:"))

@app.route("/connect2",methods=["POST"])

def connect2():
  name,code = str(request.data).strip("b").strip("'").split(",")
  id = db_man.generate_code();
  
  success = False
  error = "[unknown error]"
  
  db = db_man.init_SQL()
  game_state = db_man.game_running(db,code)
  if game_state:
    started,ended = game_state
    if started:
      error = "[game started]"
    else:
      success = True
  else:
    error = "[invalid code]"
  db_man.end_query(db)
  
  if not success:
    return(error)
  else:
    player = db_man.player(id,name,code)
    db = db_man.init_SQL()
    player.register(db)
    db_man.save(db)
    return(id)

@app.route("/create")

def create():
  return(render_template("create.html"))

@app.route("/submit_application", methods=["POST","GET"])

def submit_application():
  data = request.data
  time,date,timeadj,hours,minutes,mode = str(data).strip("b").strip("'").split(",")
  print("creating game mode [" + mode + "]")
  H,M = [int(x) for x in time.split(":")]
  y,m,d = [int(x) for x in date.split("-")]
  start = db_man.time_object(0,M,H,d,m,y) + timedelta(minutes = int(timeadj))
  start_str = datetime.strftime(start,"%d/%m/%Y %H:%M:%S")
  duration = int(hours) + int(minutes)/60
  code = db_man.generate_code()
  if db_man.is_before(datetime.now(),start):
    db = db_man.init_SQL()
    db_man.confirm_tables(db)
    game = db_man.game(start_str,duration,code,mode)
    game.register(db)
    db_man.save(db)
    return(code)
  else:
    return("!")

@app.route("/admin_test",methods=["POST","GET"])

def admin_test():
  db = db_man.init_SQL()
  print(db_man.get_codes(db))
  db_man.all_players(db)
  db_man.end_query(db)
  return(render_template("home.html"))

@app.route("/run")

def run():
  return(render_template("run.html"))

@app.route("/update_state", methods=["POST","GET"])

def update_state():
  lat,long,id = str(request.data).strip("b").strip("'").split(",")
  lat,long = float(lat),float(long)
  db = db_man.init_SQL()
  game = db_man.get_code(db,id)
  loc_string = str(lat)+","+str(long)
  game_state = db_man.game_running(db,game)
  if game_state:
    if game_state[0] and not game_state[1]:
      db_man.update_location(db,id,loc_string)
      mode = db_man.get_mode(db,game)
      db_man.save(db)
      print("mode: [" + mode + "]")
      if mode == "HaS" or mode == "Tag":
        if mode == "HaS":
          print("  >game is 'hide and seek'")
          program = modes.HideAndSeek(id)
        else:
          print("  >game is 'tag'")
          program = modes.Tag(id)
        if not program.assigned():
          program.assign_targets()
        db = db_man.init_SQL()
        try:
          targets = db_man.get_target_locations(db,id)
        except:
          targets = []
          print("error getting targets")
        db_man.save(db)
        if len(targets)>0:
          return({"info":targets})
        else:
          return("1") #no active targets
      else:
        return("2") #invalid game mode
    elif not game_state[1]:
      return("3") #game not started
    else:
      db_man.end_query(db)
      return("4") #game finished
  else:
    db_man.end_query(db)
    return("5") #game not found

@app.route("/register_catch", methods=["POST","GET"])

def register_catch():
  id = str(request.data).strip("b").strip("'")
  print("RUNNING register_catch FOR id=" + id)
  
  db = db_man.init_SQL()
  game = db_man.get_code(db,id)
  game_state = db_man.game_running(db,game)
  if game_state:
    print("  >game exists")
    if game_state[0] and not game_state[1]:
      print("  >game is running")
      db_man.save(db)
      db = db_man.init_SQL()
      mode = db_man.get_mode(db,game)
      if mode == "HaS" or mode == "Tag":
        db_man.end_query(db)
        if mode == "Has":
          print("  >game is 'hide and seek'")
          program = modes.HideAndSeek(id)
        else:
          print("  >game is 'tag'")
          program = modes.Tag(id)
        program.register_catch(id)
        print("  >registered game [exit]")
        return("5") #success
      else:
        print("  >invalid game mode [exit]")
        return("1") #invalid game mode
    elif not game_state[1]:
      print("  >game not started [exit]")
      return("2") #game not started
    else:
      db_man.end_query(db)
      print("  >game finished [exit]")
      return("3") #game finished
  else:
    db_man.end_query(db)
    print("  >game not found[exit]")
    return("4") #game not found

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(debug = True, port=port)
