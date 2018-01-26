# Salted Vex Milk
Stats and more for the ImHelping clan in D2, displayed using Django 2.0 for the back end, and bootstrap4 for the front end.

The site includes basic information about the clan as a whole, individual clan members, and links to helpful stuff (like the100). Right now it is showing generic information about the clan and players, and I am adding the stats.

Uses the third-party bootstrap4 theme [Cyborg](https://bootswatch.com/cyborg/), and for rendering sortable tables uses  [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html).

### Structure of apps
    d2api/  (core app: library for creating/processing requests)   
      |-- utils.py  (the business logic, esp the api handler)    
      |-- constants.py  (parameters like secret keys, headers)    

    clans/  (app for Clan model: generic clan info like motto)    
      |-- models.py  (the Clan model)    
      |-- forms.py  (the ModelForm for Clan)    
      |-- urls.py  (includes home page index.html)    
      |-- management/  (management function to refresh clan)
      |   |-- commands/  
      |       |-- refresh_clans.py  (updates clan info)
      |-- static/  
          |-- clans/
              |-- waterfall_movie.mp4 (movie for index.html)

    members/  (app for Member model: generic info like id)     
      |-- models.py  (the Member model)    
      |-- forms.py  (ModelForm for Member model)    
      |-- urls.py  (main page for members is /members.html)     
      |-- management/  (management function to refresh members)
          |-- commands/
              |-- refresh_members.py  (updates member info)

## To do (shorter term)
- Want table to get smaller without going to multioline, and while showing horiz scrolling. Really want to sort out tables looking nice!
- Clean up project_planning.md

- Once the above stuff (i.e., basic front-end for two pages) is working, plan how you want this organized in terms of models/pages etc (project_planning.md). For instance:
- Add characters, classes, and light levels (in components 200--so use componenets 200 to find if they have played d2).
- Start adding stats!
- Plan out models (see project_planning.md -> Models and Fields)
    - First add generic stats: light level(s), last time played, total hours played. Maybe pull with refresh members (both are part of profile 100). Put link on each player so you can pull this info for them? If so, in members use LinkColumn() (just like hasplayedd2 is a booleancolumn) or a URLColumn which renders URLs as links.
    - PvP net
	- "LIve" stats (where are they now or most recently--for whole clan this would take a loading page): https://www.reddit.com/r/django/comments/4m49r8/showing_a_loading_gif_or_message_to_the_user/
    - PvE net
    - Raid net

- For static/css stuff, check out:
https://dlo.me/archives/2013/01/14/how-to-serve-static-files-django/
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment

Questions for Jessamyn:
- How to get style sheet working? Would like to do it in svm app but seems to not work.
    https://tutorial.djangogirls.org/en/template_extending/
- load static versus load staticfiles in a template?
- When do I need urls for static files ()

## To do (longer term)


## To do in a perfect world
- x-browser testing:
    https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery/cross_browser_video_player
- Logging tune-up:
    - I don't need same `logging.basicConfig` in following files do I?
        d2api: utils
        members: views, refresh_members
        clans: views, refresh_clans I seem to be violating DRY.
    - Instead of setting level on every page, make a dictionary of levels, one for each file. Something like:
        {'refresh_clans': logging.DEBUG, 'refresh_members': logging.INFO, etc}
    Unless there a different, best-practices, approach?
    - Would be nice to have local and production configurations that I didn't have to manually change every time I wanted to go to production.
- Set up to develop on multiple computers (windows and ubuntu).
- add concurrent.futures to process multiple requests simultaneously (e.g., refresh_members)

## Static files stuff
Generally follow the instructions here:
    https://devcenter.heroku.com/articles/django-app-configuration
Tips and tricks include: try running collectstatic dry run to see how it *would* run
    heroku run python manage.py collectstatic --dry-run --noinput
To see if static file is found:
    python manage.py findstatic bootstrap.min.css --first
Note had to comment the following out because I get 500 error when it is in there:
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



## Some setup information
- Project expects your your django secret key, destiny 2 api key, and debug variable as environment variables (named `SECRET_KEY`, `D2_KEY`, and `DEBUG` respectively), which are retrieved in `settings.py` using the `get_env_variable` function).
- In `/d2api/constants.py`, set the `GROUP_ID` to the value of the clan you want to build for. It is currently set to the 'ImHelping' clan.
- Set up database settings in `settings.py`, and create database for local use, if needed. Currently uses postgres.
- To update the information about X (e.g., clan, members), at command line enter `python manage.py refresh_X`, where 'X' can be 'clan' or 'members' or whatever model you are updating. This is also the command you would enter in your scheduler (right now it configured to deploy at Heroku).

## Useful things
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), set field to clan.id, not the full clan instance.
- See  api_private_example_2 (not version controlled) for more bad url examples if you need them for testing.
- Good discussion of position: https://developer.mozilla.org/en-US/docs/Web/CSS/position
- Excellent intro to CSS: http://www.tangowithdjango.com/book/chapters/css_intro.html
- Great video conversion site: https://www.online-convert.com/
- Good for compression: https://compressify.herokuapp.com/
