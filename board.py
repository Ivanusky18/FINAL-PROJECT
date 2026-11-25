# Comment more
# Importing the pyxel library
import pyxel
# Importing the Chef class to be able to use it in the Board class
from chef import Chef
# Importing the Ingredient class
from ingredients import Ingredient
# Importing the Kitchen class
from kitchen import Kitchen
# Importing de json library to be able to read the configuration file
import json

class Board:
    """ This class contains a simple board """
    def __init__(self, file_name: str):     
        """ Method that creates the board.
        :param width: The width of the board
        :param height: The height of the board
        """

        # Opening the file
        with open(file_name, "r") as file:
            # Now data is a dictionary with all the required configuration
            self.data = json.load(file)

        # Setting the attributes
        self.width = self.data.get("board_width")
        self.height = self.data.get("board_height")

        # The board will contain a Chef in the middle of it, so one of
        # the attributes of the board will be a Chef object. Note that what is
        # at the middle of the board is the top left corner of the chef.
        self.chef = Chef(self.width // 2, 64, "upper", self.data.get("Chefs"), self.data.get("Sprites_Dimensions"))
        self.chef2 = Chef(self.width // 2, 112, "lower", self.data.get("Chefs"), self.data.get("Sprites_Dimensions"))

        # We need to set the bool to write 'Action0 in each chef when the shift is pressed

        # Creating the ingredients
        NAMES = self.data.get("names")
        self.ingredients = []
        for ingredient in NAMES:
            ingr = Ingredient(ingredient)
            self.ingredients.append(ingr)

        # This attribute will count the seconds
        self.__timer = 0

        # Creating the kitchen
        self.kitchen = Kitchen(file_name)
        self.__walkable_textures = self.data.get("walkable_textures")
        self.__textures = self.data.get("textures")
        
        # In this init we also need to initialize pyxel.
        # This instruction is used to initialize pyxel, see API for more parameters
        pyxel.init(self.width, self.height, title = "Service Rush", display_scale = 4)
        # Loading the pyxres file with the images
        pyxel.load("assets/resources.pyxres")
        # Running the game, this will call the update and draw methods in every
        # frame, see API for more
        pyxel.run(self.update, self.draw)

    # Properties
    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    # Setters
    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("The width must be an integer")
        elif width < 1:
            raise ValueError("The width must be a positive integer")
        else:
            self.__width = width

    @height.setter
    def height(self, height: int):
        if not isinstance(height, int):
            raise TypeError("The height must be an integer")
        elif height < 1:
            raise ValueError("The height must be a positive integer")
        else:
            self.__height = height

    def update(self):
        """ This is the pyxel method that gets executed in every iteration of
        the game (every frame). You need to put here all the code that has to
        be executed in every frame. Now it contains the logic to exit the
        program if Q key is pressed and to move the chef horizontally / vertically 
        if an arrow key is pressed.
        """

        # To exit the game
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        # To put the chef in the standard position when not walking    
        self.chef.walking = False
        self.chef2.walking = False

        # To move the first chef. If chef can only move in one direction at the same time: elif
        if pyxel.btn(pyxel.KEY_A) and not self.collition(self.chef.x - 1, self.chef.y):
            self.chef.move("left", self.width, self.height)
        elif pyxel.btn(pyxel.KEY_D) and not self.collition(self.chef.x + 1, self.chef.y):
            self.chef.move("right", self.width, self.height)
        elif pyxel.btn(pyxel.KEY_W) and not self.collition(self.chef.x, self.chef.y - 1):
            self.chef.move("up", self.width, self.height)
        elif pyxel.btn(pyxel.KEY_S) and not self.collition(self.chef.x, self.chef.y + 1):
            self.chef.move("down", self.width, self.height)
        # To move the second chef
        if pyxel.btn(pyxel.KEY_LEFT) and not self.collition(self.chef2.x - 1, self.chef2.y):
            self.chef2.move("left", self.width, self.height)
        elif pyxel.btn(pyxel.KEY_RIGHT) and not self.collition(self.chef2.x + 1, self.chef2.y):
            self.chef2.move("right", self.width, self.height)
        elif pyxel.btn(pyxel.KEY_UP) and not self.collition(self.chef2.x, self.chef2.y - 1):
            self.chef2.move("up", self.width, self.height)
        elif pyxel.btn(pyxel.KEY_DOWN) and not self.collition(self.chef2.x, self.chef2.y + 1):
            self.chef2.move("down", self.width, self.height)

        if not self.chef.walking:
            self.chef.walk_counter = 0
            self.chef.walk_frame = False

        if not self.chef2.walking:
            self.chef2.walk_counter = 0
            self.chef2.walk_frame = False

        # Action key for the first chef
        if pyxel.btn(pyxel.KEY_LSHIFT):
            self.chef.acting = True
        else:
            self.chef.acting = False

        # Action key for the second chef:
        if pyxel.btn(pyxel.KEY_RSHIFT):
            self.chef2.acting = True
        else:
            self.chef2.acting = False

        # We increase the timer every 30 fps
        if pyxel.frame_count % 30 == 0:
            self.__timer +=1

    def draw(self):
        """
        This is the pyxel method that gets executed in every iteration of
        the game (every frame). You need to put here all the code to draw the
        sprites of the game.
        """
        # Erasing the previous screen
        pyxel.cls(0)

        # We draw the textures
        self.kitchen.draw()
        
        # Drawing the chef. Parameters of pyxel.blt are (x, y, sprite_tuple)
        # The * is used to unpack the sprite tuple
        pyxel.blt(self.chef.x, self.chef.y, *self.chef.image, 0)

        # A text to show the position of the chef, parameters of
        # pyxel.text are (x, y, text, color)
        pyxel.text(10, 10, f"({self.chef.x}, {self.chef.y})", 7)
        # For the second chef:
        pyxel.blt(self.chef2.x, self.chef2.y, *self.chef2.image, 0)
        pyxel.text(10, 20, f"({self.chef2.x}, {self.chef2.y})", 7)

        # Showing action above the first chef:
        if self.chef.acting:
            pyxel.text(self.chef.x - 3, self.chef.y - 8, "Action", 7)

        # Showing action above the second chef:
        if self.chef2.acting:
            pyxel.text(self.chef2.x - 3, self.chef2.y - 8, "Action", 7)

        # Drawing ingredients
        y = 20
        x = 30
        for ingredient in self.ingredients:
            pyxel.blt(x, y, *ingredient.image, 0)
            x += 20

        # We draw the timer
        pyxel.text(self.width - 30, 10, "Time:" + str(self.__timer), 7)

    def collition(self, chef_x: int, chef_y: int) -> bool:
        """ Returns True if a chef placed at (chef_x, chef_y) would touch a
        texture that is not walkable """
        collition = False
        for row in range(len(self.__textures)): # This loop covers each list inside "textures"
            for column in range(len(self.__textures[row])): # This loop covers for each list inside "textures", each element
                text = self.__textures[row][column]
                x = column * 16 # This takes the x coordinate of the sprite in the layout
                y = 32 + row * 16 # This takes de y coordinate of the sprite in the layout
                # The chef (16x16) touches this texture (16x16) if both squares overlap
                touches = chef_x < x + 16 and x < chef_x + 16 and chef_y < y + 16 and y < chef_y + 16
                if touches and text not in self.__walkable_textures:
                    collition = True
        return collition