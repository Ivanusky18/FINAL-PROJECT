class Chef:
    """ It may or not have a dish. It may or not be acting """
    def __init__(self, x: int, y: int, pos: str, configuration: dict, dimensions: dict, ):
        """ Init method of the class
        :param x: the x of the chef
        :param y: the y of the chef
        :param pos: the position (x, y) of the chef
        """

        # Setting the attributes
        self.x = x
        self.y = y
        self.__configuration = configuration
        self.__dimensions = dimensions
        
        # Initially the chef will have no dish
        self.has_dish = False
                        
        # Initially the chef will not be acting
        self.acting = False

        # Initially the chef will be facing down
        self.direction = "down"    

        # The position attribute will be private, so we will not create a setter for it
        POSITIONS = ("upper", "lower")
        if not isinstance(pos, str):
            raise TypeError("The positions must be a string")
        elif pos.lower() not in POSITIONS:
            raise ValueError("The valid positions are " + str(POSITIONS))
        else:
            # We mark the position to be constant as Chefs will never change area
            self.__POSITION = pos.lower()

        # Attributes to change the image of the chef while walking
        self.walking = False # Shows if the chef is moving
        self.walk_frame = False # Which chef show
        self.walk_counter = 0 # Steps, to concadenate the 2 images without repiting the same one twice

    # Properties
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def image(self) -> tuple:
        """ The image will be a read only attribute, that will depend initially on the POSITION
        The initial sprite will be always the same, so no parameter is needed
        In Pyxel the image is a tuple with the coordinates of the image in the image bank.
        The tuple is (image_bank, starting_x, starting_y, horizontal_size, vertical_size)
        We make image a read only calculated property. 
        """
        if self.__POSITION == "upper":
            which_chef = "Chef1"
        else:
            which_chef = "Chef2"

        width = self.__dimensions["sprite_width"]
        if self.direction == "left":
            width = -width

        if self.acting:
            is_acting = "act"
        else:
            is_acting = "noact"

        if self.walking and self.walk_frame:
            is_walking = "walk"
        else:
            is_walking = "nowalk"

        chef_key = f"{which_chef}_{self.direction}_{is_acting}_{is_walking}"
        image_position = self.__configuration.get(chef_key)

        result = (0, image_position[0], image_position[1], width, self.__dimensions["sprite_height"])
        return result

    @property
    def has_dish(self) -> bool:
        return self.__has_dish

    # Setters
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("The x position must be an int")
        elif x < 0:
            raise ValueError("The x position cannot be negative")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("The y position must be an int")
        elif y < 0:
            raise ValueError("The y position cannot be negative")
        else:
            self.__y = y

    @has_dish.setter
    def has_dish(self, dish: bool):
        if not isinstance(dish, bool):
            raise TypeError("The has_dish attribute must be bool")
        else:
            self.__has_dish = dish

    # Methods
    def move(self, direction: str, board_x_size: int, board_y_size: int):
        """
        This method moves the chef. No obstacles in the board are considered.
        :param direction: a string which can be 'left' or 'right'
        :param board_x_size: the horizontal size of the board, to check the limits
        """
        # Saving the x and y positions to check if the chef has walked later
        old_x = self.x
        old_y = self.y
        DIRECTIONS = ("left", "right", "up", "down")

        # Checking the type and value of the parameters
        if not isinstance(direction, str):
            raise TypeError("The direction must be a string")
        elif not isinstance(board_x_size, int):
            raise TypeError("The board_x_size must be an integer")
        elif board_x_size < 1:
            raise ValueError("The board_x_size must be a positive integer")
        elif not isinstance(board_y_size, int):
            raise TypeError("The board_y_size must be an integer")
        elif board_y_size < 1:
            raise ValueError("The board_y_size must be a positive integer")
        elif direction.lower() not in DIRECTIONS:
            raise ValueError("The direction must be 'left', 'right', 'up' or 'down'")
        
        # We convert the direction to lower case to avoid problems with upper case letters
        direction = direction.lower()
        self.direction = direction
        
        # The (0, 0) position of the chef is the top left corner of the sprite. 
        # We can move the chef to the right if the rightmost x-coordinate of the chef is less than the board size. 
        # It will be the x-coordinate of the chef plus the width of the sprite. 
        # The width of the sprite is the 4th element of the image tuple.
        if direction == "right" and self.x + self.image[3] < board_x_size:
            self.x += 1
        # We can move the chef to the left if its x-coordinate is > 0
        elif direction == "left" and self.x > 0:
            self.x -= 1
        elif direction == "down" and self.y + self.image[4] < board_y_size:
            self.y += 1
        elif direction == "up" and self.y > 0:
            self.y -= 1

        # Checking if the chef actually moved
        if self.x != old_x or self.y != old_y:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            self.walk_counter += 1
            if self.walk_counter == 5:
                self.walk_frame = not self.walk_frame
                self.walk_counter = 0

    def act(self):
        """ This method changes the value of the acting attribute """
        self.acting = not self.acting