import database_manager as db_man
import sqlite3
from random import randint as r
from random import shuffle as rs

class HideAndSeek:
  def __init__(self,ip):
    db = db_man.init_SQL()
    self.code = db_man.get_code(db,ip)
    self.ip = ip
    self.players = {}
    for player in db_man.get_players(db,self.code):
      data = {}
      data["name"] = player[1]
      data["target"] = player[2]
      data["location"] = player[3]
      data["score"] = player[4]
      self.players[player[0]] = data
    db_man.end_query(db)

  def assigned(self):
    result = False
    for player,data in self.players.items():
      if data["target"] != "-":
        result = True
        break
    return(result)

  def assign_targets(self):
    all_players = list(self.players.keys())
    seeker = all_players[r(0,len(all_players)-1)]
    hiders = all_players
    hiders.remove(seeker)
    self.players[seeker]["target"] = hiders #I think this is superfluous, I need to redesign this function later.
    db = db_man.init_SQL()
    db_man.update_targets(db,seeker,hiders)
    db_man.save(db)
  
  def register_catch(self,id):
    print("     -REGISTERING CATCH FOR PLAYER [" + id + "]")
    db = db_man.init_SQL()
    hiders = []
    seekers = []
    all_players = db_man.get_players(db,self.code)
    all_ids = []
    for player in all_players:
      player_id = player[0]
      player_targets = player[2]
      print("     -targets of ["+ player_id + "] are " + str(player_targets))
      if player_targets != "-":
        seekers.append(player_id)
        all_ids.append(player_id)
        print("     -[" + player_id + "] is a seeker.")
      elif player_id == id:
        seekers.append(id)
        all_ids.append(id)
        print("     -[" + player_id + "] is becoming a seeker.")
      else:
        hiders.append(player_id)
        all_ids.append(player_id)
        print("     -[" + player_id + "] is a hider.")
    if len(hiders) > 0:
      for seeker in seekers:
        print("     -player [" + seeker + "] is a seeker chasing hiders " + str(hiders))
        db_man.update_targets(db,seeker,hiders)
    else:
      print("     -no hiders left, reassigning")
      hiders = []
      for player in all_ids:
        if player == id:
          print("     -not adding [" + player + "] to hiders, they are now the sole seeker")
        else:
          print("     -adding [" + player + "] to hiders")
          hiders.append(player)
      print("     -new hiders = " + str(hiders))
      print("     -new seeker = " + id)
      for hider in hiders:
        print("     -removing targets for [" + hider + "]")
        db_man.update_targets(db,hider,"-")
      db_man.update_targets(db,id,hiders)
    db_man.save(db)
    print("     -finished [back to main]")

class Tag:
  def __init__(self,id):
    db = db_man.init_SQL()
    self.code = db_man.get_code(db,id)
    self.id = id
    self.players = {}
    for player in db_man.get_players(db,self.code):
      data = {}
      data["name"] = player[1]
      data["target"] = player[2]
      data["location"] = player[3]
      data["score"] = player[4]
      self.players[player[0]] = data
    db_man.end_query(db)

  def assigned(self):
    result = False
    for player,data in self.players.items():
      if data["target"] != "-":
        result = True
        break
    return(result)
  
  def assign_targets(self):
    print("Assigning targets for gamemode [tag]")
    db = db_man.init_SQL()
    players = [player[0] for player in db_man.get_players(db,self.code)]
    rs(players)
    print(players)
    for i in range(0,len(players)-1):
      if i < len(players-1):
        db_man.update_targets(db,players[i],players[i+1])
      else:
        db_man.update_targets(db,players[i],players[0])
    db_man.save(db)
  
  def register_catch(self,id):  
    players = db_man.get_players(db,self.code)
    new_index = r(0,len(players)-1)
    timeout_count = 0
    while id == players[new_index] and timeout_count < 10:
      new_index = r(0,len(players)-1)
      timeout_count += 1
    new_target = players[new_index]
    db = db_man.init_SQL()
    db_man.update_targets(db,id,new_target)
    db_man.save()
