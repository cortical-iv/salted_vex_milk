# Salted Vex Milk
Processing clans in D2 with Django 2.0.

## Goal
Front page will have basic information about the clan. There will be pages for clan leaderboards, individual clan member stats, including what each player is currently doing.  Allow for sorting by stats. Another page for links and content (link to official clan site, to slack channel, youtube channel, strategy channels, etc).

### App structure
    |-- d2api/  (core app to make/process requests)   
    |   |-- utils.py  (api handlers/helper functions for processing responses)    
    |   |-- constants.py  (parameters like secret keys, headers)    
    |       
    |-- clans/  (app for Clan model: generic clan info like motto)    
    |   |-- models.py  (the Clan model)    
    |   |-- forms.py  (the ModelForm for Clan)    
    |   |-- urls.py  (includes home page index.html)    
    |   |-- management/  (management function to refresh clan)
    |      |-- commands/  
    |          |-- refresh_clans.py  (post request updates clan info)
    |    
    |-- members/  (app for Member model: generic info like id)     
        |-- models.py  (the Member model)    
        |-- forms.py  (ModelForm for Member model)    
        |-- urls.py  (main page for members is /members.html)     
        |   |-- management/  (management function to refresh members)
        |      |-- commands/
        |          |-- refresh_members.py  (post request updates clan info)

## To do
### General
- Automate clan update
    - Create clan management function to pull data in.
    - Automate the updates (heroku scheduler?)
- Automate members update
    - Create members management function to pull data
    - Automate that update
- Create response object like Jessamyn recommended:
    https://github.com/jessamynsmith/django-getting-started
- logging is different across multiple modules (utils and views and management
   functions: integrate into a central module?

### Clan
- Refactor utils and view (e.g., GROUP_ID is acting as a global in
    refresh_clans and probably other places.

### Member
- Store datetime the member list was last updated.
- Breaks if user tries to update members when no clan exists.
- Give option of sorting alphabetically, join date, membership type, other info.
    - Current activity (there is an 'isOnline' in the get group member endpoint), or if not online, last login.
    - Stats
- Link in members.html to each member's page with all their stats.
- constants.MEMBERSHIP_ENUM not being used.

### Scale up infrastructure built for stub version
- May need to download and use the manifest.

### Make it look non-ugly
- Bootstrap it

## In ideal world
- Should work for multiple clans, so user can enter their clan id and get this information.
- Develop on both windows and linux machine?

## Things to remember
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), you set field to model_instance.id. O
- Docs for sessions: http://docs.python-requests.org/en/master/api/#request-sessions
