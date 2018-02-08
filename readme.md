# Salted Vex Milk
Stats and more for the ImHelping clan in D2, displayed using Django 2.0 for the back end, and bootstrap4 for the front end. The site includes basic information about the clan as a whole, individual clan members, and links to helpful stuff (like the100). Right now it is showing generic information about the clan and players, and I am adding the stats.

Uses the third-party bootstrap4 theme [Cyborg](https://bootswatch.com/cyborg/), and for rendering sortable tables uses  [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html).

Currently deployed at a secret heroku site:
http://svm-dev.herokuapp.com/members/

## Management commands that need to run daily
- clan_refresh [set up to run daily]
    Basic clan info like how many members, motto, etc.
- member_refresh [set up to run daily]
    basic member info like last time they played and when they joined clan.
- character_refresh [not yet set up]
    Basic info about each character for each member of clan. Class, time played, light level. Note this is used to update member table with total time played (sums all values from characters), last time played, and highest light level.
- pvpstats_refresh [not yet set up]
    pvp stats for each member of clan.
- pvestats_refresh [not yet set up]
    pve stats for each member of clan.

## To do (shorter term)
- Organize layout of files in spyder.
- character pages: total time played is being displayed as minutes. Put in the format. Can just convert in the view and send on over. PhilsDirtyBurger will be a good corner case.
- put highest light on member page?
- pve stats needs to be fixed all the fuck up:
    - square away the floats in util like you did for pvp.
    - save/display the time variables as d/h/m like elsewhere
    - Everything is rates, so no noeed to write average or include #s (like number of suicides)
    - Clean up current columns (no need for # activities, activities cleared: and add stuff you want like strikes/nightfalls/prestige nfs/patrols or whatever).
    - Add to dropdown
    - Automate generation of dropdown menu (just give list of stats in context menu you already have that variable!): do that for pvp too.
    - Generate 'greatness' measure.
- refactor time functions into core app theyu shouldn't be just hanging in beef jerkey.
- Just make all stats pga. except stuff that can't be like num matches/ratios.
    - Be sure to explain this in page explaining stats (things like suicides and orbs are rates (suicides/game)) -- push greatness explanation there and only have very brief explanation in modal dialog.
- pvestats app (15 stats max!):
    - order thigns in a reasonable way in utils, fix it all up make it pretty.
    - Then fix strikes/heroic strikes more importantly nightfall/prestige nightfalls
        (nobody doesn't do heroic strikes: it's more about nightfalls/prestige nightfalls)
    - run refresh_pvestats
    - replicate this in the table/dropdown
    - looko over data
    - create a greatness measure
    - dance baby, dance

- Ultimately once done put raid/pvp/pve stats on character member page with character cards.
- secondsPlayed versus totalActivityDurationSeconds vs minutes played on characters? What is all this for different endpoints and such? You should really figure this shit out.
- Change to suicides per match in crucible in addition to total suicides
- All these time units are sort of fubar: some are seconds, some are minutes, some are in string and displayed as 5m 30 s (e.g., average lifespan in pve). You need to get your shit together and put all this in one format! Ultimately it has to be in numbers so it can be sorted.

## To do (when bored)
- Members.time_played: note compare to time wasted on destiny, which seems to be just PvE time played, and PvP time played spent in activity. This includes ALL time logged into characters doing anything. Note also includes AFK time, so if you do that a lot....At least explain this in about. LOok at time wasted about page it is really good.
- Permission to use figre. Get more crisp, small, version of ec59 image.
- Make sure units in pve and pvp are the same (e.g., suicide pga/total)
- Set up refresh_characters to run on heroku.
- Make better logging message when person hasn't played d2 it makes it seem catastrophic
- Make sure there is consistgent naming for endpoint helper functions (extract_X) not (make_list) or whatever, make it consiste.

## To do (when done with stuff above)
- Consider a mega management command that runs all the listed management commands. Why have them all run separately?
- Put some kind of image on stats pages (pvp pve raid icons). Good visual indicator of what is up.
- Did I need a separate character app? Well, it is definitely a separate model so why not. But maybe not a separate page: make 'characters' page part of a 'member' page, and have their stats, with characters as just one part of it. Should display total time played, other stats.

## To do (maybe)
- Set up to show who is playing right now (though not what they are doing :)), with warning this could take a little while. Will require concurrency almost guaranteed: https://devcenter.heroku.com/articles/optimizing-dyno-usage
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
