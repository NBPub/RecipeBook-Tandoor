# RecipeBook - Tandoor
Python web-app (Flask) to browse [Tandoor](https://docs.tandoor.dev/) recipes on the local network. Designed for use with E-Ink screens. 

For a version that works with [Nextcloud Cookbook](https://apps.nextcloud.com/apps/cookbook),  please navigate to [RecipeBook](https://github.com/NBPub/RecipeBook)

[Deploy with Docker](https://github.com/NBPub/RecipeBook-Tandoor#application-setup) • [Local Build](https://github.com/NBPub/RecipeBook-Tandoor#build-locally) • [Screenshots](https://github.com/NBPub/RecipeBook-Tandoor#screenshots) • [Upcoming](https://github.com/NBPub/RecipeBook-Tandoor#upcoming)

## Overview

I created this to access recipes from [Tandoor](https://docs.tandoor.dev/) and easily view them on Kindle's web browser whilst cooking. The view is designed for such screens, and is not as nice as the actual app. Therefore, accessing your Tandoor website with a mobile device or tablet would just as effectively provide kitchen access to your recipes. This project is not associated with Tandoor.

Please note that the web application is very basic and should not be run on untrusted networks. It is not designed to be exposed publicly.

The application reads data from Tandoor using its API, and a valid token must be provided. This is (an extension of) my first project using Flask and building Docker containers. Feedback is appreciated.

### Supported Architectures

Pulling from DockerHub should provide the correct image for your system. The application is built on the python-alpine base image. The "tandoor" tag is necessary to pull the version build for use with Tandoor. See [DockerHub Repository](https://hub.docker.com/r/nbpub/recipelook),

Images are available for the following architectures:

| Architecture | 
| :----: | 
| x86-64 |
| arm64 | 
| armhf |

## Application Setup

Install and run using docker, examples provided below. See [LinuxServer.io](https://docs.linuxserver.io/) and [Docker](https://docs.docker.com/) for more information on Docker containers.

Access main page at `<your-ip>:5000`. See [below](https://github.com/NBPub/RecipeBook-Tandoor#parameters) for changing port number.

### Usage  
    
This container uses data from your Tandoor instance by calling its API. Therefore, an appropriate API Token and URL are required for it to function. Data for the homepage will be saved, and only refreshing the data will require a valid token and URL. However, each recipe-page needs to use the API, and therefore Tandoor must be accessible.

Find your API Token at `http://<your-URL>/settings/#api`

Example configurations to build container are shown below. Some Environmental Variables are listed with default values and do not need to be specified, `Token` and `URL` must be correctly set for the application to function. Healthcheck is optional.

### docker-compose

```yaml
---
version: "2"
services:
  recipe:
    image: nbpub/recipelook:tandoor
    container_name: recipebook
    ports:
      - 5000:5000
    environment:
      - TZ=America/Los_Angeles
      - PAGE_TITLE=Recipe Book
      - FONT_SMALL=30
      - FONT_LARGE=36
      - Token=PasteYourTokenHere
      - URL=http://localhost:8080/
    healthcheck:
      test: curl -I --fail http://localhost:5000 || exit 1
      interval: 300s
      timeout: 10s
      start_period: 5s
    restart: unless-stopped
```

### docker cli ([click here for more info](https://docs.docker.com/engine/reference/commandline/cli/))

```bash
docker run -d \
  --name=recipebook \
  -e TZ=America/Los_Angeles \
  -e PAGE_TITLE=Recipe Book \
  -e FONT_SMALL=30 \
  -e FONT_LARGE=36 \
  -e Token=PasteYourTokenHere
  -e URL=http://localhost:8080/
  -p 5000:5000 \
  --restart unless-stopped \
  nbpub/recipelook:tandoor
```

### Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 5001:5000` would expose port `5000` from inside the container to be accessible from the host's IP on port `5001` outside the container.

| Parameter | Function |
| :----: | --- |
| `-p 5000:5000` | Default Flask port. Internal port should not be changed. |
| `-e TZ=America/Los_Angeles` | Set timezone for logging using tzdata. |
| `-e PAGE_TITLE=Recipe Book` | Home page title. Displays on tab. |
| `-e FONT_SMALL=30` | Default size for "small" sections: **Description** and **Keywords**. Can be changed to any `<integer>` to adjust web-page display. |
| `-e FONT_LARGE=36` | Default size for "large" sections: **Steps** data. Can be changed to any `<integer>` to adjust web-page display. |
| `-e Token=PasteYourTokenHere` | Default Token is an empty string. API calls will not work unless a valid token is provided. |
| `-e URL=http://localhost:8080/` | Default URL for Tandoor instance. This should be changed to the appropriate base URL for Tandoor. |

  

## Upcoming

**Version 1.0** is released. If issues are found or enhancements dreamt, they will come here until pushed to a new version.

I do not use Tandoor, and built this application with recipes downloaded from the [demo website](https://app.tandoor.dev/). Therefore, many features may not be supported. Please open an issue if you have ideas for improvements or bug-fixes. Listed below are some limitations I am aware of, but there are likely many others I have not encountered. Thank you for your help!

**Known Limitations**
* Support for non-text based Steps (Type = time / file / recipe)
* Ratings and comments <- should be easy to integrate

**Possible Future Improvements**
* Provide option to not load images by default. Restore image button will still be present.
* Cache recipe data to reduce needed API calls, provide functionality without accessing Tandoor
  * More local storage vs Less network traffic

* Clean up exception handling code
* wget instead of curl for healthchecks - does this provide smaller docker image?
* keyword handling
* Add tests
* clean up CSS styling
* Volume binding for configuration folder, let user poke through directories


## Screenshots

<details>
  <summary>Home Page, lists all recipes</summary>
  
  ![Home](/Screenshots_Kindle/homepage.png "Home Page")
</details>

<details>
  <summary>Filter Button</summary>
    
  ![Home](/Screenshots_Kindle/category_filter.png "Filter Button")
</details>

<details>
  <summary>Text Search, recipe titles only</summary>
    
  ![Home](/Screenshots_Kindle/searchbar.png "Search Bar")
</details>

<details>
  <summary>Recipe Page example, with image</summary>
    
  ![Home](/Screenshots_Kindle/recipe_Image.png "Image")
</details>


<details>
  <summary>Recipe Page example, without image</summary>
    
  ![Home](/Screenshots_Kindle/recipe_NoImage.png "No Image")
</details>


<details>
  <summary>Recipe Page example, single Step</summary>
    
  ![Home](/Screenshots_Kindle/recipe_SingleStep.png "Single Step Recipe")
</details> 


<details>
  <summary>Recipe Page example, multipe Steps</summary>
    
  ![Home](/Screenshots_Kindle/Recipe_MultiStep1.png "Multiple Steps 1/2")
</details> 

<details>
  <summary>Recipe Page example, multipe Steps continued</summary>
    
  ![Home](/Screenshots_Kindle/Recipe_MultiStep2.png "Multiple Steps 2/2")
</details> 

<details>
  <summary>Error Page - Invalid API Token</summary>
    
  ![Home](/Screenshots_Kindle/error_API.png "Invalid API Token")
</details> 

<details>
  <summary>Error Page - Invalid URL</summary>
    
  ![Home](/Screenshots_Kindle/error_URL.png "Host cannot be reached")
</details> 

## Build Locally
    
*Instructions may not be comprehensive. Docker deployment is recommended.*

If you want to run RecipeBook without Docker, a python virtual environment is recommended. See [Flask Installation](https://flask.palletsprojects.com/en/2.0.x/installation/) for more details (and appropriate commands for Windows). [Python 3.7](https://wiki.python.org/moin/BeginnersGuide/Download) or newer is recommended.

1. [Download](https://github.com/NBPub/RecipeBook-Tandoor/archive/refs/heads/main.zip) the code in the repository. Click the green code button at the top of the page for options.

2. Extract the folder contents. Copy the files+folders within "app" directory and "requirements.txt" to a new directory. Keep "ExampleRecipes" folder if you want to test with example data. All other contents can be deleted.

3. Move to newly made directory and create and activate **venv**.

```
$ cd newdirectory
$ python -m venv venv
$ . venv/bin/activate
```

4. Install Flask, dependencies.

```
$ pip install -r requirements.txt
```

5. Adjust Flask parameters as desired, see [Flask Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/). A **Flask Env** file saves some typing when running the application. For example, if you only want the server to be visible from the local machine, remove `FLASK_RUN_HOST=0.0.0.0` from the file. The port number (default, 5000) can be changed in this file, too.

```
$ nano .flaskenv
```

*Additionally, it can be used to set values to environmental variables, as described in [Docker Parameters](https://github.com/NBPub/RecipeBook-Tandoor#parameters). Additions to base code may be required for this step (python-dotenv package, `load_dotenv()`). Note that all local variables associated with environmental variables can be modified by changing the code. See next step for an example*

6. Modify URL and API-Token variables. See lines 15 and 19 of [Tandoor_Reader.py](https://github.com/NBPub/RecipeBook-Tandoor/blob/main/app/Tandoor_Reader.py). `URL=<put your Tandoor URL here>` and `Token=<put your token here>`

7. Run! Open site in web browser (http://localhost:5000). 

```
$ flask run
```

8. Press Ctrl+C to stop server. Deactivate **venv** when finished.

```
$ deactivate
```

