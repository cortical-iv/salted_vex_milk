# Salted Vex Milk
Processing clans in D2 with Django 2.0.

Front page will have basic information about the clan and clan members. Should include leaderboards, individual clan member stats, including what each player is currently doing. Another page for links and content (link to official clan site, to slack channel, youtube channel, strategy channels, etc).

Currently it's just a stub that shows basic clan information and member information (e.g., join date), as I work out the basic architecture.

### Structure of apps
    d2api/  (core app: library for creating/processing requests)   
      |-- utils.py  (the business logic, esp the api handler)    
      |-- constants.py  (parameters like secret keys, headers)    

    clans/  (app for Clan model: generic clan info like motto)    
      |-- models.py  (the Clan model)    
      |-- forms.py  (the ModelForm for Clan)    
      |-- urls.py  (includes home page index.html)    
      |-- management/  (management function to refresh clan)
          |-- commands/  
              |-- refresh_clans.py  (updates clan info)

    members/  (app for Member model: generic info like id)     
      |-- models.py  (the Member model)    
      |-- forms.py  (ModelForm for Member model)    
      |-- urls.py  (main page for members is /members.html)     
      |-- management/  (management function to refresh members)
          |-- commands/
              |-- refresh_members.py  (updates member info)

## To do (shorter term)
- That hamburger people will not know what to do with it. Need a 'how to' for the site? Put link other than home in collapsed version. Change it to say "menu", or just show the menus you only have like four right now. progressively collapsing navigations (maybre scrollable). tabs with a 'more' section that basically is a dropdown menu to remaining tabs. Good article:
https://medium.com/@kollinz/hamburger-menu-alternatives-for-mobile-navigation-a3a3beb555b8
Principles I want to follow:
-Words not icons.
-Have everything there don't make them scroll. So...dropdown menu with 'more' (e.g., about, etc)
- At some point handle video size better: make it depend on size of viewing window: have two sizes. 480, and then 620 for viewing windows larger than 700 or whatever.
- Members page:
    - Why do I need to add spacing to header? And is it different in firefox deployed? Why are fonts rendered differently in firefox@heroku but not chrome?
- Implement jessamyn's suggestions about heroku settings.py bits.
-  Create style sheet and link to it.

- Once the above stuff (i.e., basic front-end for two pages) is working, plan how you want this organized in terms of models/pages etc (project_planning.md). For instance:
- Add characters, classes, and light levels (in components 200--so use componenets 200 to find if they have played d2).
- Start adding stats!
- Plan out models (see project_planning.md -> Models and Fields)
    - First add generic stats: light level(s), last time played, total hours played. Maybe pull with refresh members (both are part of profile 100). Put link on each player so you can pull this info for them? If so, in members use LinkColumn() (just like hasplayedd2 is a booleancolumn) or a URLColumn which renders URLs as links.
    - PvP net
	- "LIve" stats (where are they now or most recently--for whole clan this would take a loading page): https://www.reddit.com/r/django/comments/4m49r8/showing_a_loading_gif_or_message_to_the_user/
    - PvE net
    - Raid net


## To do (longer term)


## To do in a perfect world
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

## Static files
-Try running collectstatic dry run and it seems fine.
    heroku run python manage.py collectstatic --dry-run --noinput
First followed instructions here, and put movie in project folder instead of app folder:
    https://devcenter.heroku.com/articles/django-assets
It made no difference, so I went back to app folder way, which seems better.
Note had to comment this out because I get 500 error when it is in there:
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
https://devcenter.heroku.com/articles/django-app-configuration



## Some setup information
- Store your django secret key and destiny 2 api key as environment variables (named `SECRET_KEY` and `D2_KEY`, respectively, which are retrieved in `settings.py` using the `get_env_variable` function).
- In `/d2api/constants.py`, set the `GROUP_ID` to the value of the clan you want to build for. It is currently set to cortical_iv's clan.
- Set up database settings in `settings.py`, and create database for local use, if needed. Currently uses postgres.
- To update the information about X (e.g., clan, members), at command line enter `python manage.py refresh_X`, where 'X' can be 'clan' or 'members' right now. This is also the command you would enter in your scheduler (right now it configured to deploy at Heroku).

## Useful things
- In extract_member_info, be sure to use mke_request, and not the api_handler, as the latter doesn't differentiate between bungie errors and server errors, and you use the bungie error to tell if user has played d2.
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), set field to clan.id, not the full clan instance.
- Docs for sessions: http://docs.python-requests.org/en/master/api/#request-sessions
- See  api_private_example_2 (not version controlled) for more bad url examples.
