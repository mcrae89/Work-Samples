# Nathan Mead

class Ingredient:
    '''Represent an Ingredient for cooking

    attribtues: name, quantity, measurement
    '''
    
    def __init__(self, name = '', quantity = 0, measurement = ''):
        ''' Initializes a new Ingredient object

        name: str
        quantity: int or float
        measurement: str
        '''
        self.name = name
        self.quantity = quantity
        self.measurement = measurement

    def get_name(self):
        return self.name
    
    def get_quantity(self):
        return self.quantity

    def get_measure(self):
        return self.measurement

    def __str__(self):
        return '%s %s of %s' % (self.quantity, self.measurement, self.name)

    def add_to_shopping_list(self):
        raise NotImplementedError('Not implemented in Ingredient')

class IngredientOnHand(Ingredient):
    '''Represents an Ingredient object that is available for use
    '''

    def __init__(self, name = '', quantity = 0, measurement = ''):
        Ingredient.__init__(self, name, quantity, measurement)

    def add_to_shopping_list(self):
        return False

class IngredientFromStore(Ingredient):
    '''Represents an Ingredient object that  is at the store
    '''
    
    def __init__(self, name = '', quantity = 0, measurement = ''):
        Ingredient.__init__(self, name, quantity, measurement)

    def add_to_shopping_list(self):
        return True

if __name__ == '__main__':
    ingredient1 = Ingredient('Flour', 1, 'cup')
    print(ingredient1)
    ioh1 = IngredientOnHand('Cornmeal' , 1, 'cup')
    print(ioh1)
    ios1 = IngredientFromStore('Salt', 1, 'tsp')
    print(ios1)
