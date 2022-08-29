from backend import data
from random import randint

valid_modes = ["HaS","Tag"]

class HaS:
  def __init__(self,player,game):
    self.player = player
    self.game = game
    self.players = []
    self.ids = []
    self.hiders = []
    self.seekers = []
    self.assigned = False
    for player in game.players:
      self.players.append(data.player(player))
      self.ids.append(player)
    for player in self.players:
      if player.targets == []:
        self.hiders.append(player.code)
      else:
        self.seekers.append(player.code)
        self.assigned = True
        
  def assign_targets(self):
    seeker_index = randint(0,len(self.ids)-1)
    seeker_id = self.ids[seeker_index]
    seeker = self.players[seeker_index]
    print("seeker:",seeker.name)
    self.hiders = self.ids
    self.hiders.remove(seeker_id)
    seeker.update(targets=self.hiders)

  def adjust_targets(self):
    if self.player.code in self.hiders:
      if len(self.hiders) > 1:
        self.hiders.remove(self.player.code)
        self.seekers.append(self.player.code)
        for seeker in self.seekers:
          seeker = data.player(seeker)
          seeker.update(targets=self.hiders)
      else:
        self.hiders = self.seekers
        self.seekers = [self.player.code]
        for hider in self.hiders:
          hider = data.player(hider)
          hider.update(targets=[""])
        self.player.update(targets = self.hiders)

  def get_info(self):
    my_json = {"names":[],"locations":[]}
    targets = self.player.targets
    for target in targets:
      target = data.player(target)
      my_json["names"].append(target.name)
      my_json["locations"].append((target.lat,target.long))
    return(my_json)

class Tag:
  def __init__(self,player,game):
    self.player = player
    self.game = game
    self.players = []
    self.ids = []
    self.assigned = False
    for player in game.players:
      self.players.append(data.player(player))
      self.ids.append(player)
    for player in self.players:
      if player.targets != []:
        self.assigned = True
        break