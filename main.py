from objects.game import Game


def play_game():
    game = Game()
    while not game.is_game_over():
        game.player_move(input())
    print("GAME OVER!")


if __name__ == "__main__":
    play_game()
