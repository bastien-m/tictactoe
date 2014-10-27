import Model.MorpionModel as Model
import View.MorpionView as View


class MorpionController:

    def __init__(self, first_player="player1", second_player="player2"):
        self.model = Model.MorpionModel(first_player, second_player)
        self.view = View.MorpionView(self.model.board, self)
        self.current_player = self.model.player1
        self.winner = None

    def lay_down(self, position_x, position_y):
        try:
            self.winner = self.model.attribute_player_to_block(position_x, position_y, self.current_player)
            self._change_player()
            if self.winner:
                return self.winner
        except Exception as e:
            raise e

    def _change_player(self):
        if self.current_player == self.model.player1:
            self.current_player = self.model.player2
        else:
            self.current_player = self.model.player1

    def start_game(self):
        self.view.start_rendering()