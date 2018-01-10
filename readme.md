# Salted Vex Milk
Processing clans in D2 with Django 2.0.

Front page will have basic information about the clan and clan members. Should include leaderboards, individual clan member stats, including what each player is currently doing. Another page for links and content (link to official clan site, to slack channel, youtube channel, strategy channels, etc).

Currently it's just a stub that shows basic clan information and member information (e.g., join date), as I work out the basic architecture.

### Structure of apps
    d2api/  (core app: library for creating/processing requests)   
      |-- utils.py  (the business logic)    
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
- Add characters, classes, and light levels (in components 200--so use componenets 200 to find if they have played d2).
- Start adding stats!
- Plan out models (see project_planning.md -> Models and Fields)
    - First add generic stats: light level(s), last time played, total hours played. Maybe pull with refresh members (both are part of profile 100). Put link on each player so you can pull this info for them?
    - PvP net
	- "LIve" stats (where are they now or most recently--for whole clan this would take a loading page)
    - PvE net
    - Raid net


## To do (longer term)
- Work on front end (bootstrap)
- Testing. Make some urls that will generate different types of errors for unit testing. Note you can use httpbin.org too:
    - make_request
        - InvalidUrl: 'foo'
        - InvalidHttp: 'foo.com'
        - 400: https://bungie.net/Platform/Destiny2/SearchDestinyPlayer/2/&-@#/
        - 500: https://www.bungie.net/admin/
    - process_bungie_request:
        - KeyError: need a way to produce a bungie error
    - refresh_clans

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
- Make 'clans' app 'clan', as it is baked into this app that there is one clan. this is actually sort of a pain in the ass and not important.



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
