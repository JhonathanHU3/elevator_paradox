import traceback
import sys
from core.game import Game

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print("Error occurred:")
        print(traceback.format_exc())
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()  