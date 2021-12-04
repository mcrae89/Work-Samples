#Nathan Mead
#Final Program

from Ingredient import *
from Recipe import *

name = input('Please enter a name for this recipe: ').capitalize() # used to set the name of the recipe

on_hand_list = []
from_store_list = []

def ingre_list(): # used to request and compile a list of ingredients
    global on_hand_list
    global from_store_list
    ingre_list = []
    ingre1 = Ingredient(input('\nPlease enter the name of the first ingredient: ').capitalize(), input('Please enter the amount needed: '),
                        input('Please enter the measurement of this amount. (cups, tsp, etc.): '))  # requests the first ingredient
    ingre_list.append(ingre1) # adds to ingredient list for use in recipe
    on_hand = input('Do you have this ingredient on hand?') # determines if an ingredient needs to be added to the shopping list
    if on_hand == 'yes':
        on_hand_list.append(ingre1)
    else:
        from_store_list.append(ingre1)
    more = 'yes' # placeholder
    while more != 'no': # used to loop the ingredient request
        ingre = Ingredient(input('\nPlease enter the name of the next ingredient: ').capitalize(), input('Please enter the amount needed: '), input('Please enter the measurement of this amount. (cups, tsp, etc.): '))
        ingre_list.append(ingre)
        on_hand = input('Do you have this ingredient on hand? ')
        if on_hand == 'yes':
            on_hand_list.append(ingre)
        else:
            from_store_list.append(ingre)
        more = input('\nDo you have more ingrendients to add? ')
        if more == 'no': # breaks the loop if user inputs that no additional ingredients are needed
            break
    return ingre_list

def instruct_list(): # used to request and compile a list of instructions
    instruct_list = []
    instruct1 = input('\nPlease enter the the first step: ').capitalize() # request the first instruction
    instruct_list.append(instruct1) # adds to instruction use for use in recipe
    more = 'yes'
    while more != 'no': # used to loop the instruction request
        instruct = input('Please enter the the next step: ').capitalize()
        instruct_list.append(instruct)
        more = input('\nDo you have more intructions to add? ')
        if more == 'no': # breaks the loop if user inputs that no additional instructions are needed
            break
    return instruct_list

ingre_list = ingre_list() # calls the ingre_list function and assigns it to variable

instruct = instruct_list() # calls the instruct_list function and assigns it to variable

print()
recipe = Recipe(name, ingre_list, instruct) # creates a new recipe object using the user inputed information
print(recipe)
print()
print('Shopping List:')
for c in from_store_list: # prints the items that needs to be purchased
    print(c)
