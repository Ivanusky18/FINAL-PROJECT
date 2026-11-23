#Comment more
# We need to import the library to be able to read the config.json
from pathlib import Path
from board import Board

# First we need to construct the path to the configuration file, it will be relative
# to the path of this main file: it will be in assets/config.json
file_name = str(Path(__file__).parent / "assets" / "config.json")

# Creating the board object will also initialize pyxel
board = Board(file_name)