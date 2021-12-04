# Nathan Mead

from Ingredient import *

class Recipe:
    '''Represents a Recipe object.

    attributes: name, ingredients, instructions
    '''

    def __init__(self, name = '', ingredients = '', instructions = ''):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def getName(self):
        return self.name

    def getIngredients(self):
        return self.ingredients

    def getInstructions(self):
        return self.instructions

    def __str__(self):
        res = []
        inst = []
        for c in self.ingredients: # runs through the list of ingredients and adds them in a more printable format
            res.append(str(c))
        for c in self.instructions: # runs through the list of instructions and adds them in a more printable format
            inst.append(str(c))
        return self.name + '\n' + '\n' + '\nIngredients:\n' + '\n'.join(res) + '\n' + '\n' + '\nInstructions:\n' + '\n'.join(inst) # formats how the recipe should print out



if __name__ == '__main__':
    ingre1 = Ingredient('Flour' , 1 , 'cup')
    ingre2 = Ingredient('Sugar', 1/2, 'cup')
    ingre_list = (ingre1, ingre2)
    instr1 = 'Put the fluor into a medium sized bowl'
    instr2 = 'Put the sugar into the same bowl as the flour'
    instr_list = (instr1, instr2)
    recipe1 = Recipe('Cookies', ingre_list, instr_list)
    print(recipe1)
