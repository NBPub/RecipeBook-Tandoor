from pathlib import Path
import json
import pickle as pickle
from shutil import copy
import requests

def TandoorParser(API, headers):
    
    RecipeNames = {}
    RecipeCategories = {}
    PageNames = {}
    ImagePaths = {}
    RecipeDescriptions = {}
    Instructions = {}
    Ingredients = {}
    
    try:
        if requests.get(''.join([API,'user-name']), headers=headers, timeout=0.5).status_code == 403: # Catch 403 for invalid token
            error = ''.join([requests.get(''.join([API,'user-name']), headers=headers).json()['detail'], ' - Check provided API token'])
            return error
        else:
            Recipes = requests.get(''.join([API,'recipe']), headers=headers, timeout = 2).json() # if 200 return, try to get data

            for i in range(Recipes['count']): # Minus 2 included to omit multi-step recipes, for now
                data = Recipes['results'][i]
                ID = data['id']
                RecipeNames[ID] = (data['name'])
                ImagePaths[ID] = (data['image'])
                RecipeDescriptions[ID] = (data['description'])
                SafeName = "".join(char for char in data["name"] if char.isalnum() or char == ' ')
                PageNames[SafeName.replace(' ','')] = ID # Save above name without spaces for URLs
                
                RecipeCat = []
                for j in range(len(data['keywords'])):
                    RecipeCat.append(data['keywords'][j]['label'])
                RecipeCategories[ID] = (','.join(RecipeCat))
                
            del data, Recipes

            with open(Path(Path.cwd(), 'TandoorData.pkl'), 'wb') as f:
                pickle.dump([RecipeNames, RecipeCategories, PageNames, ImagePaths, RecipeDescriptions], f)
            error = ''
            return error
            
    except requests.exceptions.ConnectionError as error:
        error = 'Failed to reach host - Check Tandoor URL' # if host URL cannot be reached, return error page
        return error
    except Exception as error:
        return error # other errors? will print on error page