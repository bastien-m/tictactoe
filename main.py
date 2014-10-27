import Controller.MorpionController as Controller

if __name__ == "__main__":
    game_controller = Controller.MorpionController("Player1", "Player2")
    game_controller.start_game()