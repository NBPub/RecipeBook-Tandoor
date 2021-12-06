from flask import Flask

app = Flask(__name__)

from pathlib import Path
import json
from flask import render_template, request
import pickle as pickle
from os import environ
import requests
from Tandoor_Parser import TandoorParser


# Load Environmental Variables
URL =  environ.get('URL','http://localhost:8080/')
if URL[-1:] != '/':
    URL = ''.join([URL,'/']) # Add trailing slash, if needed

Token =  environ.get('Token','')

API = ''.join([URL,'api/'])
headers = {'Authorization': f'Token {Token}'}

#Load in Environmental Variables
HomePageTitle =  environ.get('PAGE_TITLE','Recipe Book')
LargeFont =  f'{environ.get("FONT_LARGE","36")}px'
SmallFont =  f'{environ.get("FONT_SMALL","30")}px'

# Function to parse recipe data, refresh to parse recipe folder if changes are made
def Refresh():
    if Token != '':
        error = TandoorParser(API, headers)
    else:
        error = 'No API token provided'
    return error


# Landing Page, list of recipes
# POST methods for refresh  or returning to category functions
@app.route("/", methods = ['GET','POST'])
@app.route("/recipes/", methods = ['GET','POST'])
def homepage():
    if not(Path(Path.cwd(), 'TandoorData.pkl').exists()): # Initial data load, provide error page if unsuccessful
        error = Refresh()
        if error != '':
            app.logger.error('Invalid API token and/or URL provided, set as environmental variables and restart app')
            app.logger.error(error)
            return render_template('errorTandoor.html', URL=URL, SmallFont=SmallFont, HomePageTitle=HomePageTitle, error=error, LargeFont=LargeFont)
         
    if request.method == 'POST':
        if request.form.get('reload') == 'Refresh List':
            error = Refresh()
            if error != '':
                app.logger.error(error)
                app.logger.error('Recipe data not refreshed . . . Invalid API token and/or URL provided, set as environmental variables and restart app')
        if request.form.get('cat-select') != None:
            ActiveCat = request.form.get('cat-select')
        else:
            ActiveCat = 'Show all'
    else:
        ActiveCat = 'Show all'
        
    with open(Path(Path.cwd(), 'TandoorData.pkl'), 'rb') as f: # Load list of recipes for homepage display
        RecipeNames, RecipeCategories, PageNames, ImagePaths, RecipeDescriptions = pickle.load(f)
    del f, ImagePaths, RecipeDescriptions
    
    Categories = {} # unique categories for filter buttons
    i = 0
    for value in RecipeCategories.values():
        items = value.split(',')
        for item in items:
            Categories[item] = i
            i +=1 
    Categories = list(set(Categories))
    Categories.insert(0,'Show all') # Add show all button
    
    return render_template('landingTandoor.html', RecipeNames=RecipeNames, ActiveCat=ActiveCat, \
                           PageNames=PageNames, HomePageTitle=HomePageTitle, \
                           Categories=Categories, RecipeCategories=RecipeCategories)


# Recipes Page, gather data from specific recipe call (/api/recipe/ID)
@app.route('/recipes/<page>', methods = ['GET','POST'])
def showpage(page):
    # Check for no data, attempt refresh
    if not(Path(Path.cwd(), 'TandoorData.pkl').exists()):
        error = Refresh()
        if error != '':
            app.logger.error('Invalid API token and/or URL provided, set as environmental variables and restart app')
            return render_template('errorTandoor.html', URL=URL, SmallFont=SmallFont, HomePageTitle=HomePageTitle, error=error, LargeFont=LargeFont)     
        
   # Double-Check if API/URL functioning. Likely can wrap this in function and elimate step
   # Case: where parsed data exists, but container is launched with invalid API/URL. Will catch error before continuing to recipe data fetch
    else:
        try:
            if requests.get(''.join([API,'user-name']), headers=headers, timeout = 0.5).status_code == 403:    
                error = ''.join([requests.get(''.join([API,'user-name']), headers=headers).json()['detail'], ' - Check provided API token'])
                app.logger.error(error)
                return render_template('errorTandoor.html', URL=URL, SmallFont=SmallFont, HomePageTitle=HomePageTitle, error=error, LargeFont=LargeFont)
        except requests.exceptions.ConnectionError as error:
            error = 'Failed to reach host - Check Tandoor URL'
            app.logger.error(error)
            return render_template('errorTandoor.html', URL=URL, SmallFont=SmallFont, HomePageTitle=HomePageTitle, error=error, LargeFont=LargeFont)
        except Exception as error:
            app.logger.error(error)
            return render_template('errorTandoor.html', URL=URL, SmallFont=SmallFont, HomePageTitle=HomePageTitle, error=error, LargeFont=LargeFont)
    
    # If all works, open saved data. Find recipe index to fill in the rest.
    with open(Path(Path.cwd(), 'TandoorData.pkl'), 'rb') as f:
        RecipeNames, RecipeCategories, PageNames, ImagePaths, RecipeDescriptions = pickle.load(f)
    del f
   
    index = PageNames[page] # recipe index to fetch associated data
    title = RecipeNames[index] # name
    category = RecipeCategories[index].split(',') # keyword(s)
    description = RecipeDescriptions[index] # description
    
    if request.method == 'POST': # Add or remove image if button is pressed
        if request.form.get('imswitch') == 'Remove Image':
            image = ''
        elif request.form.get('imswitch') == 'Restore Image':
            image = ImagePaths[index]
    elif request.method == 'GET': # Default: provide image, if exists
        if index in ImagePaths:
            image = ImagePaths[index]
        else:
            image = ''
    del RecipeNames, RecipeCategories, PageNames, ImagePaths, RecipeDescriptions
    
    # API call to fetch recipe steps
    Steps = requests.get(''.join([API,'recipe/',str(index)]), headers=headers).json()['steps']
    
    instructions = {}
    ingredients = {}
    step_names = {}
    for i in range(len(Steps)):
        data = Steps[i]
        if data['name'] == '':
            step_names[i+1] = f'Step {i+1}'
        else:
            step_names[i+1] = data['name']        
        
        Instructions = data['instruction'].split('\n')
        instructions[i+1] = Instructions
        
        Ingredients = []
        for j in range(len(data['ingredients'])):
            Item = data['ingredients'][j]
            if Item["amount"] == 0:
                amount = ''
            else:
                amount = Item["amount"]
            if Item["unit"]:
                unit = Item["unit"]["name"]
            else:
                unit = ''
            Ingredients.append(f'{amount} {unit} {Item["food"]["name"]} {Item["note"]}')
        if Ingredients != []:
            ingredients[i+1] = Ingredients

    del Steps, data, Instructions, Ingredients
    
    return render_template('recipeTandoor.html', LargeFont=LargeFont, SmallFont=SmallFont, \
                           category=category, page=page, title=title, image=image, \
                           description=description, ingredients=ingredients, \
                           instructions=instructions, step_names=step_names)

@app.route("/favicon.ico")
def favicon():
    image = "favicon.ico"
    return render_template('imageTandoor.html', image=image)    
