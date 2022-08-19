import database_manager as db_man
import sqlite3
from random import randint as r

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
    self.players[seeker]["target"] = hiders
    db = db_man.init_SQL()
    db_man.update_targets(db,seeker,hiders)
    db_man.save(db)
  
  def register_catch(self,id):
    db = db_man.init_SQL()
    hiders = []
    seekers = []
    for player in all_players:
      data = db_man.get_players(db,self.code)
      player_id = data[0]
      player_targets = data[2]
      if len(player_targets) > 0 or player_id == id:
        seekers.append(id)
      else:
        hiders.append(id)
    for seeker in seeker:
      db_man.update_targets(db,seeker,hiders)
    db_man.save(db)
