class MorpionModel:
    _FIRST_PLAYER_LABEL = 1
    _SECOND_PLAYER_LABEL = 4
    _NUMBER_OF_LINE = 3

    def __init__(self, player1, player2):
        """
        :param player1: String name of the first player
        :param player2: String name of the second player
        :return: Instance of MorpionModel
        """
        self.player1 = player1
        self.player2 = player2
        self.board = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]


    def attribute_player_to_block(self, block_x, block_y, player):
        assert self.player1 == player or self.player2 == player, 'Player Must be a known player'

        if self.board[block_y][block_x] != 0:
            raise Exception("This block is not free")


        if self.player1 == player:
            self.board[block_y][block_x] = self._FIRST_PLAYER_LABEL
        else:
            self.board[block_y][block_x] = self._SECOND_PLAYER_LABEL

        winner = self._check_winner()
        return winner

    def _check_winner(self):
        for y in range(len(self.board)):
            count_by_column = 0
            count_by_line = 0
            for x in range(len(self.board[0])):
                count_by_line += self.board[y][x]
                count_by_column += self.board[x][y]
            if count_by_line == self._FIRST_PLAYER_LABEL * self._NUMBER_OF_LINE \
                    or count_by_column == self._FIRST_PLAYER_LABEL * self._NUMBER_OF_LINE:
                return self.player1
            elif count_by_line == self._SECOND_PLAYER_LABEL * self._NUMBER_OF_LINE \
                    or count_by_column == self._SECOND_PLAYER_LABEL * self._NUMBER_OF_LINE:
                return self.player2

        count_by_diagonal = 0
        count_by_other_diagonal = 0
        for i in range(len(self.board)):
            count_by_diagonal += self.board[i][i]
            count_by_other_diagonal += self.board[i][-1 - i]
        if count_by_diagonal == self._FIRST_PLAYER_LABEL * self._NUMBER_OF_LINE \
                or count_by_other_diagonal == self._FIRST_PLAYER_LABEL * self._NUMBER_OF_LINE:
            return self.player1
        elif count_by_diagonal == self._SECOND_PLAYER_LABEL * self._NUMBER_OF_LINE \
                or count_by_other_diagonal == self._SECOND_PLAYER_LABEL * self._NUMBER_OF_LINE:
            return self.player2
        return None