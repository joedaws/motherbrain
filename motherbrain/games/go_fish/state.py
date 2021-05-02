from motherbrain.players.go_fish import GoFishPlayer
from motherbrain.games.core.game import GameState
from motherbrain.games.core.deck_builder import DeckBuilder
from motherbrain.brains.spaces.go_fish.observations import Observations


class GoFishState(GameState):
    """A class representing the state of the go fish game."""

    get_deck = DeckBuilder('motherbrain.games.go_fish', 'card').build_deck

    def __init__(self, num_players=4):
        player_names = ['player ' + str(i) for i in range(num_players)]
        self.players = {GoFishPlayer(name): i for i, name in enumerate(player_names)}
        self._set_player_indices()
        self.opponents_map = self._setup_opponents_map()

        self.deck = self.get_deck()

        self.observations = {player: Observations(player, self.opponents_map[player])
                             for player in self.players}

        self._observers = []

    def reset(self):
        """Reset to an initial state."""
        self.deck = self.get_deck()
        self.observations = {player: Observations(player, self.opponents_map[player])
                             for player in self.players}

    def hands(self):
        """Returns hands of all players.

        Returns:
            dictionary whose keys are players and whose values are the corresponding player's hand.
        """
        return {player: player.hand for player in self.players}

    def update(self, event):
        """update the state according to the event."""

        # update observations
        for player in self.players:
            self.observations[player].update(event)

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.notify()

    def _set_player_indices(self):
        """Set the index attribute of the players."""
        for player, index in self.players.items():
            player.index = index

    def _setup_opponents_map(self):
        """Create a dictionary describing the opponents of each players."""
        indices = list(self.players.values())
        return {player: [opponent for opponent in self.players if opponent != player] for player in self.players}
