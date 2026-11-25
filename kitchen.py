#Comment more
import json
import pyxel

class Kitchen:
    def __init__(self, file_name: str):

        # Opening the file
        with open(file_name, "r") as file:
            # Now data is a dictionary with all the required configuration
            data = json.load(file)

        # Setting the attributes
        self.__textures = data.get("textures")
        self.__sprites = data.get("sprites")
        self.__dimensions = data.get("Dimensions")
        self.__non_blocking_textures = data.get("non_blocking_textures")
        self.__board_height = data.get("board_height")

        self.__scanned = self.scan()

    def scan(self):
        result = []
        for row in range(len(self.__textures)):
            for column in range(len(self.__textures[row])):
                text = self.__textures[row][column]
                x = column * 16
                y = 32 + row * 16
                result.append((text, x, y))
        return result
    
    def draw(self):
        '''This method is used to draw each texture where it belongs'''
        for text, x, y in self.__scanned: # In each turn it takes a tuple of three elements: text, x and y
            sprite = self.__sprites[text]
            pyxel.blt(x, y, 0, sprite[0], sprite[1], self.__dimensions[0], self.__dimensions[1])

    def collision(self) -> list:
        self.__blockers_positions = []
        for text, x, y in self.__scanned:
            if text in self.__blocking_textures:
                self.__blockers_positions.append((x, y))
        return self.__blockers_positions