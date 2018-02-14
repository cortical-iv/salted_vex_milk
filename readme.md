# Salted Vex Milk
Stats and more for Echo Company 59 clan in D2. Created with Django 2.0 for the back end and Bootstrap4 for the front end. The site includes pve/pvp leaderboards, basic information about the clan and its members, and some links that people in the clan might find helpful. Uses the third-party bootstrap theme [Cyborg](https://bootswatch.com/cyborg/) and renders tables using [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html). It is currently deployed at heroku: http://saltedvexmilk.herokuapp.com.

## Some notes on setup
- Project expects your your django secret key, destiny 2 api key, and debug variable as environment variables (named `SECRET_KEY`, `D2_KEY`, and `DEBUG` respectively), which are retrieved in `settings.py` using the `get_env_variable` function).
- In `/d2api/constants.py`, set the `GROUP_ID` to the value of the clan you want to build for.
- Set up database settings in `settings.py`, and create database for local use, if needed. Currently uses postgres.
- To update the info in each model, run `python manage.py refresh_database` from your virtual environment. This is also the command you would enter in your scheduler at heroku.

## To do for beta deploy
- Tomorrow see if it ran at 4am
- Set DEBUG to false.
- Update this and blast off.

## Wish list
- Custom 404 page.
- When stats change, currently have to change the list of stats in tables/models/forms/utils/views/template dropdown.
- Add prestige nightfalls. Bungie may add this endpoint: https://github.com/Bungie-net/api/issues/304
- Do proper x-browser testing:  https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery/cross_browser_video_player


### Project structure (folders in project root directory)
	salted_vex_milk
      |-- management/  (runs all other management commands)
      |   |-- commands/  
      |       |-- refresh_database.py  (runs all other refresh commands updates entire db)

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

    pvestats/  (app for PveStats model: stats from pve like stories and raids)     
      |-- models.py  (the PveStats model)    
      |-- forms.py  (PveStatsForm for PveStats model)    
      |-- urls.py  (pages for pve stats are /pvestats/<stat>/)     
      |-- management/  (management function to refresh stats)
          |-- commands/
              |-- refresh_pvestats.py  (updates stats for each member info)

    pvpstats/  (app for PvpStats model: stats from pvp like k/d and trials matches)     
      |-- models.py  (the PvpStats model)    
      |-- forms.py  (PvpStatsForm for PvpStats model)    
      |-- urls.py  (main page for pvp stats are /pvpstats/<stat>/)     
      |-- management/  (management function to refresh stats)
          |-- commands/
              |-- refresh_pvpstats.py  (updates stats for each member info)  

    d2api/  (core app for creating/processing requests)for future   
      |-- utils.py  (the business logic, esp the api handler)    
      |-- constants.py  (parameters like secret keys, headers)   

    static/  (files used by everything)
      |-- bootstrap.min.css (cyborg custom bootstrap4 theme)
      |-- style.css (home-grown styles for the pages)

## Acknowledgments
Thanks to [Jessamyn Smith](https://www.codementor.io/jessamynsmith) at codementor who helped me navigate the Django labyrinth while making this project. Thanks to members of EC59 for general advice about the site, and to the Destiny2 developer community. Thanks to Bungie for making a great game and providing the API to developers.
