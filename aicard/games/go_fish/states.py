from aicard.players.go_fish import GoFishPlayer
from aicard.games.core.deck import Deck
from aicard.games.core.events import ExchangeEvent, BookEvent, DrawEvent
from aicard.brains.spaces.go_fish import ObservationSpace


class GoFishState:
    """A class representing the state of the go fish game."""
    def __init__(self, num_players=4):
        player_names = ['players'+str(i) for i in range(num_players)]
        self.players = {i: GoFishPlayer(name) for i, name in enumerate(player_names)}
        self._set_player_indices()
        self.opponents_map = self._setup_opponents_map()

        self.deck = Deck()

        self.player_observations = {i: ObservationSpace(self.opponents_map[i])
            for i in self.players.keys()}

    def hands(self, player_indices=None):
        """Returns hands of all of or a subset of players.

        Args:
            player_indicies (list): A list of integers corresponding to the hands
                of the players which you want to see.
        """
        if player_indices is None:
            # return all players hands
            player_indices = list(self.players.keys())

        return {i: player.hand for i, player in self.players.items() if i in player_indices}

    def update(self, event):
        """update the state according to the event."""
        if isinstance(event, BookEvent):
            pass
        elif isinstance(event, ExchangeEvent):
            pass
        elif isinstance(event, DrawEvent):
            pass

    def _set_player_indices(self):
        """Set the index attribute of the players."""
        for index, player in self.players.items():
            player.index = index 

    def _setup_opponents_map(self):
        """Create a dictionary describing the opponents of each players."""
        indices = list(self.players.keys())
        return {i: [j for j in indices if j != i] for i in indices}