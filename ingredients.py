#Comment more
class Ingredient:
    def __init__(self, name: str):
        """ Init method of the class
        :param name: the name of the ingredient
        """

        # Setting the attributes
        self.name = name

        # Initially the ingredients will not be chopped
        self.chopping = False

    # Properties
    @property
    def name(self) -> str:
        return self.__name

    # We make image a read only attribute, so we eliminate the setter
    @property
    def image(self) -> tuple:
        if not self.chopping:  # Here we must do the same as we did in chef.
            if self.name == "chorizo":
                result = (0, 48, 32, 16, 16)
            elif self.name == "tomato":
                result = (0, 0, 32, 16, 16)
            elif self.name == "onion":
                result = (0, 32, 32, 16, 16)
            elif self.name == "potato":
                result = (0, 16, 32, 16, 16)
            elif self.name == "egg":
                result = (0, 64, 32, 16, 16)
        else:
            if self.name == "chorizo":
                result = (0, 48, 48, 16, 16)
            elif self.name == "tomato":
                result = (0, 0, 48, 16, 16)
            elif self.name == "onion":
                result = (0, 32, 48, 16, 16)
            elif self.name == "potato":
                result = (0, 16, 48, 16, 16)
            elif self.name == "egg":
                result = (0, 64, 48, 16, 16)
        return result

    # Another way is to use a dictionary

    # Setters
    @name.setter
    def name(self, value: str):
        INGREDIENTS = ("tomato", "potato", "onion", "chorizo", "egg")
        if not isinstance(value, str):
            raise TypeError("The ingredient name must be a string")
        elif value.lower() not in INGREDIENTS:
            raise ValueError("The valid names are " + str(INGREDIENTS))
        else:
            self.__name = value.lower()

    def cut(self, status: str):
        """ This method cuts the ingredients 
        :param status: indicates whether the ingredient is or not cut
        """
        STATUS = ("cut", "not cut")
        if not isinstance(status, str):
            raise TypeError("The status must be a string")
        elif status.lower() not in STATUS:
            raise ValueError("The status must be in status")
        
        if status == "cut" or self.chopping == True: # and cut_table_position == True:
            self.chopping = True