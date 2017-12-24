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
        |-- management/  (management function to refresh members)
           |-- commands/
               |-- refresh_members.py  (post request updates member info)

## To do
- Check heroku logs next few says make sure scheduler worked.
- Remove buttons form pages.
- Remove manager commands from views: they aren't needed anymore.
- Create response object:
    https://github.com/jessamynsmith/django-getting-started
- logging is different across multiple modules (utils and views and management
   functions: integrate into a central module?
- Email log files?
    https://stackoverflow.com/a/6187851/9072894
- In footer of members.html, sho datetime the list was last updated
    - Set as a class attribute ((*not* instance attribute)
    - Put in template
- GROUP_ID is acting as a global (views and management fncts): fix this

### Member to do
- Breaks if user tries to update members when no clan exists.
- Give option of sorting alphabetically, join date, membership type, other info.
    - Current activity (there is an 'isOnline' in the get group member endpoint), or if not online, last login.
    - Stats
- Link in members.html to each member's page with all their stats.
- constants.MEMBERSHIP_ENUM not being used.

### Make it look non-ugly
- Bootstrap it

## In ideal world
- Should work for multiple clans, so user can enter their clan id and get this information.
- Develop on both windows and linux machine?

## Things to remember
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), you set field to model_instance.id. O
- Docs for sessions: http://docs.python-requests.org/en/master/api/#request-sessions
