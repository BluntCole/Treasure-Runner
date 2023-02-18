from GameEngine import GameEngine
from GameObject import MyGameObject

engine = GameEngine()
engine.add_game_object(MyGameObject())
engine.start()