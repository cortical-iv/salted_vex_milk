# Salted Vex Milk
Stats and more for the ImHelping clan in D2, displayed using Django 2.0 for the back end, and bootstrap4 for the front end. The site includes basic information about the clan as a whole, individual clan members, and links to helpful stuff (like the100). Right now it is showing generic information about the clan and players, and I am adding the stats.

Uses the third-party bootstrap4 theme [Cyborg](https://bootswatch.com/cyborg/), and for rendering sortable tables uses  [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html).

Currently deployed at a secret heroku site:
http://svm-dev.herokuapp.com/members/

## To do (shorter term)
- PvP stats:
    - Start with default (either pvpstats/kd or pvpstats/all), then let user select.
    - Add link to each user and bring to individual user page that shows all their stats. Maybe put this *below* their character cards? It would just be a two column table after all.
    - Give option to filter by number of matches (>0, > 10, > 50, > 100)
- Should just make 'characters' page a 'member' page, and have their stats, with characters as just one part of it. Should display total time played, other stats.

## To do (when bored)
- Character app: set up refresh_characters to run on heroku.
- Make better logging message when person hasn't played d2 it makes it seem catastrophic
- Members page maybe have table-sm for smaller screens, but not for larger screens?
- Change units of time displayed to days/hours/minutes instead of minutes (both on members screen and on character cards on characters.html).
- ONce leaderboards are set, set up time played leaderboard?
- Make sure there is consistgent naming for endpoint helper functions (extract_X) not (make_list) or whatever, make it consiste.
- Add dropdown headers/dividers to the 'useful' dropdown (and change name of 'useful' to something more informative)
- Add counter column to leaderboard tables: https://stackoverflow.com/questions/37694971/how-to-add-counter-column-in-django-tables2
- Add page numbers to bottom of pages:
https://stackoverflow.com/questions/16409236/displaying-page-numbers-with-django-tables2


## To do (maybe)
- Set up to show who is playing right now, with warning this could take a little while. Will require concurrency almost guaranteed: https://devcenter.heroku.com/articles/optimizing-dyno-usage
- x-browser testing:
    https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery/cross_browser_video_player
- Set up to develop on multiple computers (windows and ubuntu).

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
