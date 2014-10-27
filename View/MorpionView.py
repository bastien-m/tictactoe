import pygame
import sys
import time
import threading

class MorpionView():
     #----- constants -----#
    _NUMBER_OF_BOX_BY_LINE = 3
    _LINE_WIDTH = 2
    _WINDOW_WIDTH = 500
    _WINDOW_HEIGHT = 500
    _MARGIN_X = 50
    _MARGIN_Y = 50
    _MARGIN_INNER = 2
    _BOX_X = (_WINDOW_WIDTH - _MARGIN_X * 2 - _MARGIN_INNER * 2) / _NUMBER_OF_BOX_BY_LINE
    _BOX_Y = (_WINDOW_HEIGHT - _MARGIN_Y * 2 - _MARGIN_INNER * 2) / _NUMBER_OF_BOX_BY_LINE
    _LINE_MARGIN = 10
    _CENTER_CIRCLE = (_BOX_X / 2., _BOX_Y / 2.)
    _CIRCLE_RADIUS = round((_BOX_X - _LINE_MARGIN * 2) / 2.)
    _FPS = 30

    def __init__(self, board, controller):
        """
        init the view by linking the game controller to the view
        then does additional treatments using pygame
        to initialize the game engine
        :param board: MorpionController instance
        :return:
        """
        pygame.init()
        self.winner = None
        self.board = board
        self.controller = controller
        self._fps_clock = pygame.time.Clock()
        self._DISPLAY_SURF = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT))
        pygame.display.set_caption('Tic tac toe game')
        self._define_color()
        self.win_music = pygame.mixer.Sound('resources/win.wav')

    def _define_color(self):
        """
        Just a method called to define all the color used in the
        tic tac toe board
        :return:
        """
        self._SECOND_PLAYER_COLOR = (12, 67, 232)
        self._FIRST_PLAYER_COLOR  = (136, 14, 255)
        self._WHITE = (255, 255, 255)
        self._BACKGROUND_COLOR = (26, 140, 255)

    def _draw_scene(self):
        """
        draw the scene by checking the board model (fill all in white)
        :return:
        """
        self._DISPLAY_SURF.fill(self._BACKGROUND_COLOR)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                position_x = self._MARGIN_X + x * (self._BOX_X + self._MARGIN_INNER)
                position_y = self._MARGIN_Y + y * (self._BOX_Y + self._MARGIN_INNER)
                pygame.draw.rect(self._DISPLAY_SURF, self._WHITE, (position_x, position_y, self._BOX_X, self._BOX_Y))
                if self.board[y][x] == 1:
                    #pygame.draw.rect(self._DISPLAY_SURF, self._GREEN, (position_x, position_y, self._BOX_X, self._BOX_Y))
                    self._draw_cross(x, y, self._FIRST_PLAYER_COLOR)
                elif self.board[y][x] == 4:
                    #pygame.draw.rect(self._DISPLAY_SURF, self._BLUE, (position_x, position_y, self._BOX_X, self._BOX_Y))
                    self._draw_circle(x, y, self._SECOND_PLAYER_COLOR)

    def _draw_cross(self, x, y, color):
        _x = self._MARGIN_X + x * (self._MARGIN_INNER + self._BOX_X)
        _y = self._MARGIN_Y + y * (self._MARGIN_INNER + self._BOX_Y)
        beginning_line_point = (_x + self._LINE_MARGIN, _y + self._LINE_MARGIN)
        ending_line_point = (_x + self._BOX_X - self._LINE_MARGIN, _y + self._BOX_Y - self._LINE_MARGIN)
        pygame.draw.aaline(self._DISPLAY_SURF, color, beginning_line_point, ending_line_point, self._LINE_WIDTH)

        #second line
        _x = self._MARGIN_X + x * (self._MARGIN_INNER + self._BOX_X)
        _y = self._MARGIN_Y + y * (self._MARGIN_INNER + self._BOX_Y) + self._BOX_Y
        beginning_line_point = (_x + self._LINE_MARGIN, _y - self._LINE_MARGIN)
        ending_line_point = (_x + self._BOX_X - self._LINE_MARGIN, _y - self._BOX_Y + self._LINE_MARGIN)
        pygame.draw.aaline(self._DISPLAY_SURF, color, beginning_line_point, ending_line_point, self._LINE_WIDTH)

    def _draw_circle(self, x, y, color):
        x = self._MARGIN_X + x * (self._MARGIN_INNER + self._BOX_X)
        y = self._MARGIN_Y + y * (self._MARGIN_INNER + self._BOX_Y)
        center_circle_point = (int(x + self._CENTER_CIRCLE[0]), int(y + self._CENTER_CIRCLE[1]))
        pygame.draw.circle(self._DISPLAY_SURF, color, center_circle_point, self._CIRCLE_RADIUS, self._LINE_WIDTH)

    def _handle_click(self):
        """
        retrieve mouse position and perform action to get the clicked block
        :return:
        """
        mouse_position = pygame.mouse.get_pos()
        block = self._get_block(mouse_position)

        if block:
            x = block[0]
            y = block[1]
            try:
                self.winner = self.controller.lay_down(x, y)
                if self.winner:
                    sound_thread = threading.Thread(None, self._play_win_sound, (), {})
                    sound_thread.start()
                    print("You win : {player}".format(player=self.winner))
            except Exception as e:
                print(e)
                print('Try another place')


    def _play_win_sound(self):
        self.win_music.play()
        time.sleep(1.5)
        self.win_music.stop()

    def _get_block(self, mouse_position):
        """
        did some calculation about the mouse position to retrieve
        the corresponding block
        :param mouse_position: the mouse position during the click event
        :return: None if none or block if found
        """
        position_mouse_x = mouse_position[0]
        position_mouse_y = mouse_position[1]

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                block_x = self._MARGIN_X + x * (self._BOX_X + self._MARGIN_INNER)
                block_y = self._MARGIN_Y + y * (self._BOX_Y + self._MARGIN_INNER)
                if block_x < position_mouse_x < block_x + self._BOX_X \
                        and block_y < position_mouse_y < block_y + self._BOX_Y:
                    return x, y
        return None

    def start_rendering(self):
        """
        the main loop of the game
        in charge of rendering and intercepting all the event
        :return:
        """
        while not self.winner:
            self._draw_scene()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click()

            pygame.display.update()

            self._fps_clock.tick(self._FPS)