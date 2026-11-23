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


    
    def draw(self):
        '''This method is used to draw each texture where it belongs'''
        for row in range(len(self.__textures)):
            for column in range(len(self.__textures[row])):
                text = self.__textures[row][column]
                x = column * 16
                y = 32 + row * 16
                sprite = self.__sprites[text]
                pyxel.blt(x, y, 0, sprite[0], sprite[1], self.__dimensions[0], self.__dimensions[1]) # I don't know if self.__dimensions is going to work propertly