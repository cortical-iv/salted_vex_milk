# Salted Vex Milk
Stats and more for the ImHelping clan in D2, displayed using Django 2.0 for the back end, and bootstrap4 for the front end. The site includes basic information about the clan as a whole, individual clan members, and links to helpful stuff (like the100). Right now it is showing generic information about the clan and players, and I am adding the stats.

Uses the third-party bootstrap4 theme [Cyborg](https://bootswatch.com/cyborg/), and for rendering sortable tables uses  [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html).

Currently deployed at a secret heroku site:
http://svm-dev.herokuapp.com/members/

## Management commands that need to run daily
- refresh_clans [set up]
    Basic clan info like how many members, motto, etc.
- refresh_members [set up]
    basic member info like last time they played and when they joined clan.
- refresh_characters [not yet set up]
    Basic info about each character for each member of clan. Class, time played, light level. Note this is used to update member table with total time played (sums all values from characters), last time played, and highest light level.
- refresh_pvpstats [not yet set up]
    pvp stats for each member of clan.
- refresh_pvestats [not yet set up]
    pve stats for each member of clan.

## To do
- Make better logging message when person hasn't played d2 it makes it seem catastrophic
- Put pvp/pve stats on character member page in separate cards.
- Put some kind of image on stats pages (pvp pve raid icons). Good visual indicator of what is up.
- Set up all refresh commands to run on heroku: why not just set up a mega command that updates *everything*? That's all you care about right? Put it in the core app.

## Final refactoring walkthrough
- Make sure order in 'all' tables is same as order in dropdowns
- Make sure all stat names, dropdown descriptions, and column verbose names are the same in pvp/pve.
- Make sure there is consistgent naming for endpoint helper functions (extract_X) not (make_list) or whatever, make it consiste.
- Set logging settings to be reasonable.


## To do (maybe, or next project)
- It is super inefficient to have to change the list of stats in tables, models, forms, utils, views, and template dropdown when you make a single change in your stat(s). This is a gross violation of DRY. It would be *really* nice to fix this.
- Set up to develop on multiple computers (windows and ubuntu).
- Prestige nightfalls: check getactivityhistory for one of bruin's characters:
Need characterid, userid, membershiptype, count (100 or whatever), mode (17=heroic), page (starts with 0). Heroic completion *percentage* would be cool to have. Basically can't look at 'completed' that is 1 if they time out, need to look at score.
    - wait on this thorn is looking into it:
    https://github.com/Bungie-net/api/issues/304


- Add all stats to dropdown: automate this you already have list of stats as dropdown (but note it isn't that simple there is actual value, and display value). Have two lists, one of display one of variable name, combine them and pass in context, loop through and create dropdown menu that way. Doing this shit by hand is fucking crazy.
- x-browser testing:
    https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery/cross_browser_video_player


### Project structure (folders in root directory)
    clans/  (app for Clan model: generic clan info like motto)    
      |-- models.py  (the Clan model)    
      |-- forms.py  (the ModelForm for Clan)    
      |-- urls.py  (includes home page index.html)    
      |-- management/  (management function to refresh clan)
      |   |-- commands/  
      |       |-- refresh_clans.py  (updates clan info)
      |-- static/  (movies in multiple formats for index.html -- and an image for loser browsers)
          |-- clans/
              |-- waterfall_color.mp4
              |-- waterfall_color.webm
              |-- waterfall_color.ogv
              |-- waterfall_color.jpg

    members/  (app for Member model: generic info like id)     
      |-- models.py  (the Member model)    
      |-- forms.py  (ModelForm for Member model)    
      |-- urls.py  (main page for members is /members.html)     
      |-- management/  (management function to refresh members)
          |-- commands/
              |-- refresh_members.py  (updates member info)

    d2api/  (core app for creating/processing requests)   
      |-- utils.py  (the business logic, esp the api handler)    
      |-- constants.py  (parameters like secret keys, headers)   

    static/  (general stuff that each app uses)
      |-- bootstrap.min.css (cyborg custom bootstrap4 theme)
      |-- style.css (home-grown styles for the pages)

##Acknowledgments
Thanks to [Jessamyn Smith](https://www.codementor.io/jessamynsmith) at codementor who helped me navigate the Django labyrinthe while making this project.

## Questions for Jessamyn:
- load static versus load staticfiles in a template? I seem to never need load staticfiles
- is it ok to do initial management file, but then I need additional information from character refresh before I can finish filling it in is this ok?


## Some setup information
- Project expects your your django secret key, destiny 2 api key, and debug variable as environment variables (named `SECRET_KEY`, `D2_KEY`, and `DEBUG` respectively), which are retrieved in `settings.py` using the `get_env_variable` function).
- In `/d2api/constants.py`, set the `GROUP_ID` to the value of the clan you want to build for. It is currently set to the 'ImHelping' clan.
- Set up database settings in `settings.py`, and create database for local use, if needed. Currently uses postgres.
- To update the information about X (e.g., clan, members), at command line enter `python manage.py refresh_X`, where 'X' can be 'clan' or 'members' or whatever model you are updating. This is also the command you would enter in your scheduler (right now it configured to deploy at Heroku).


## Useful things
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), set field to clan.id, not the full clan instance.
- See  api_private_example_2 (not version controlled) for more bad url examples if you need them for testing.
- Excellent intro to CSS: http://www.tangowithdjango.com/book/chapters/css_intro.html
- Good discussion of position: https://developer.mozilla.org/en-US/docs/Web/CSS/position
- Great video conversion site: https://www.online-convert.com/
- Good for compression: https://compressify.herokuapp.com/
