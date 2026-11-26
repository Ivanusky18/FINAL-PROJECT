import pyxel

class Kitchen:
    def __init__(self, textures: dict, sprites: dict, dimensions: dict):

        # Setting the attributes
        self.__textures = textures
        self.__sprites = sprites
        self.__dimensions = dimensions

    # Properties
    @property
    def textures(self) -> dict:
        return self.__textures

    # Methods
    def draw(self):
        """ This method is used to draw each texture where it belongs """
        result = []
        for key in self.__textures:
            row = int(key) 
            for column in range(len(self.__textures[key])): # This loop covers for each list inside "textures", each element
                text = self.__textures[key][column]
                x = column * 16 # This takes the x coordinate of the sprite in the layout
                y = 32 + row * 16 # This takes de y coordinate of the sprite in the layout# In each turn it takes a tuple of three elements: text, x and y
                sprite = self.__sprites[text]
                pyxel.blt(x, y, 0, sprite[0], sprite[1], self.__dimensions["sprite_width"], self.__dimensions["sprite_height"])
                result.append((text, x, y))
        return result