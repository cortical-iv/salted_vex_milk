# Salted Vex Milk
Processing clans in D2 with Django 2.0.

Front page will have basic information about the clan and clan members. Should include leaderboards, individual clan member stats, including what each player is currently doing. Another page for links and content (link to official clan site, to slack channel, youtube channel, strategy channels, etc).

Currently it's just a stub that shows basic clan information and member information (e.g., join date), as I work out the basic architecture.

### Structure of apps
    d2api/  (core app to make/process requests)   
      |-- utils.py  (the business logic)    
      |-- constants.py  (parameters like secret keys, headers)    

    clans/  (app for Clan model: generic clan info like motto)    
      |-- models.py  (the Clan model)    
      |-- forms.py  (the ModelForm for Clan)    
      |-- urls.py  (includes home page index.html)    
      |-- management/  (management function to refresh clan)
          |-- commands/  
              |-- refresh_clans.py  (post request updates clan info)

    members/  (app for Member model: generic info like id)     
      |-- models.py  (the Member model)    
      |-- forms.py  (ModelForm for Member model)    
      |-- urls.py  (main page for members is /members.html)     
      |-- management/  (management function to refresh members)
          |-- commands/
              |-- refresh_members.py  (post request updates member info)

## To do
- Check heroku logs next few days make sure scheduler worked (12/24/17).
- In footer of members.html, show datetime the list was last updated
    - Set as a class attribute ((*not* instance attribute)
    - Put in template
- Resuscitate response object:
    https://github.com/jessamynsmith/django-getting-started
- GROUP_ID is acting as a global (views and management fncts): fix this
- Refactor member class/view
    - Breaks if user tries to update members when no clan exists.
    - Give option of sorting alphabetically, join date, membership type, other info.
        - Current activity (there is an 'isOnline' in the get group member endpoint), or if not online, last login.
        - Stats
    - Link in members.html to each member's page with all their stats.
- Work on front end make it less ugly bootstrap.
- Centralize logger settings: they are defined separately in
    utils/views/management

## In ideal world
- Should work for multiple clans, so user can enter their clan id and get this information.
- How to set up to develop on both windows and linux machine?

## Things to remember
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), set field to model_instance.id.
- Docs for sessions: http://docs.python-requests.org/en/master/api/#request-sessions
