"""
The core game class which other games inherit from
"""
from __future__ import annotations # will become default in py3.10
from abc import ABC, abstractmethod
import pickle
from motherbrain.games.core import LIBRARY_PATH
from motherbrain.games.core.scribe import GameScribe
import os


class Game:
    """
    Base Game class defining the common methods and attributes for games.

    Be sure to either set _state in the init method of all child classes
    of this class or use super().__init__ in the child class __init__.
    """
    def __init__(self, *args, **kwargs):
        self._state = None
    
    @property
    def state(self) -> GameState:
        return self._state

    @state.setter
    def state(self, new_state: GameState) -> None:
        self._state = new_state


class GameState(ABC):
    """
    Base GameState class defining common methods and attributes for the stae of a game.
    """
    @abstractmethod    
    def attach(self, observer: GameStateObserver) -> None:
        """
        Attach a game observer to this game.
        """
        pass

    @abstractmethod
    def detach(self, observer: GameStateObserver) -> None:
        """
        Detach an observer from this game.

        Note: It is not clear that an observer will ever be detached.
        This is implemented just for better practice in implementing 
        the observer design pattern.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify the observer of an event.
        """
        pass


class GameStateObserver(ABC):
    """
    Base Game state Observer class
    """
    LIBRARY_PATH = LIBRARY_PATH

    def __init__(self):
        self._id = '0000'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @abstractmethod
    def update(self, game_state: GameState):
        """
        receive updates from the game state.
        """
        pass

    def write_to_library(self, game_name, history, tag=None):
        """
        write history to file
        
        TODO in the future, allow for writting to 
        remote source such as S3 bucket.
        """
        scribe = GameScribe()
        scribe.history = history
        if tag:
            scribe.tag = tag
        artifact_path = os.path.join(self.LIBRARY_PATH, game_name, self.id+'.pkl')
        scribe.save(artifact_path)
        

