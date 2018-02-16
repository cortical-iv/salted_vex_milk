# Salted Vex Milk
Stats and more for Echo Company 59 clan in D2. Created with Django 2.0 for the back end and Bootstrap4 for the front end. The site includes pve/pvp leaderboards, basic information about the clan and its members, and some links that people in the clan might find helpful. Uses the third-party bootstrap theme [Cyborg](https://bootswatch.com/cyborg/) and renders tables using [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html). It is currently deployed at heroku: http://saltedvexmilk.herokuapp.com.

## Some notes on setup
- Project expects your your django secret key, destiny 2 api key, and debug variable as environment variables (named `SECRET_KEY`, `D2_KEY`, and `DEBUG` respectively), which are retrieved in `settings.py` using the `get_env_variable` function).
- In `/d2api/constants.py`, set the `GROUP_ID` to the value of the clan you want to build for.
- Set up database settings in `settings.py`, and create database for local use, if needed. Currently uses postgres.
- To update the info in each model, run `python manage.py refresh_database` from your virtual environment. This is also the command you would enter in your scheduler at heroku.
- When deploying, set DEBUG to false, or at heroku to the empty string.
- Natural refresh order for database: clans->members->characters->pvestats->pvpstats


## Wish list
- Add last time played pvp/pve to leaderboards: would involve GetActivityHistory over all characters, count=1 (most recent), mode (either pvp or pve) and page=0. Then parse activities,period which is easy to parse as a datetime like all the others. Best to quickly do it while updating characters rather than while updating pvp/pve stats.
- Adjustable number of rows: keep at 10 but give user a dropdown menu that feeds it in through the url or via a get request. https://stackoverflow.com/a/35518016/9072894
- Add prestige nightfalls. Bungie may add this endpoint: https://github.com/Bungie-net/api/issues/304
- When stats change, currently have to change the list of stats in tables/models/forms/utils/views/template dropdown, violating DRY.


### Project structure (folders in project root directory)
	salted_vex_milk (core app also contains settings, urls.py, etc)
      |-- management/  (runs all other management commands)
      |   |-- commands/  
      |       |-- refresh_database.py  (runs all other refresh commands updates entire db)
	  	|-- templates/salted_vex_milk/
			|   |-- 404.html    
			|-- static/salted_vex_milk/
			    |-- misadventure.png (404 image)

    clans/  (app for Clan model: generic clan info like motto)    
      |-- models.py  (the Clan model)    
      |-- forms.py  (the ModelForm for Clan)    
      |-- urls.py  (includes home page index.html)    
      |-- management/  (management function to refresh clan)
      |   |-- commands/  
      |       |-- refresh_clans.py  (updates clan info)
			|-- templates/clans/
			|   |-- base.html    
			|   |-- index.html   
			|   |-- about.html   
			|-- static/clans/
          |-- waterfall_color.mp4
          |-- waterfall_color.webm
          |-- waterfall_color.ogv
          |-- waterfall_color.jpg
					|-- ec59.png (for about page)
          |-- favicon.ico  (site favicon)
          |-- salt.png (alt icon for about page)			

    members/  (app for Member model: generic info like id)     
      |-- models.py  (the Member model)    
      |-- forms.py  (ModelForm for Member model)    
      |-- urls.py  (main page for members is /members.html)  
			|-- templates/members/
			|   |-- members.html		   
      |-- management/  (management function to refresh members)
          |-- commands/
              |-- refresh_members.py  (updates member info)

    pvestats/  (app for PveStats model: stats from pve like stories and raids)     
      |-- models.py  (the PveStats model)    
      |-- forms.py  (PveStatsForm for PveStats model)    
      |-- urls.py  (pages for pve stats are /pvestats/<stat>/)     
      |-- management/  (management function to refresh stats)
      |   |-- commands/
      |       |-- refresh_pvestats.py  (updates stats for each member info)
			|-- templates/pvestats/
			|   |-- pvestats.html
			|-- static/pvestats/
          |-- pve_icon.png  (little image for top of leaderboard)



    pvpstats/  (app for PvpStats model: stats from pvp like k/d and trials matches)     
      |-- models.py  (the PvpStats model)    
      |-- forms.py  (PvpStatsForm for PvpStats model)    
      |-- urls.py  (main page for pvp stats are /pvpstats/<stat>/)     
      |-- management/  (management function to refresh stats)
      |   |-- commands/
      |       |-- refresh_pvpstats.py  (updates stats for each member info)  
			|-- templates/pvpstats/
			|   |-- pvpstats.html
			|   |-- memberpvp.html (not used single player stat table)
			|-- static/pvpstats/
          |-- pvp_icon.png  (little image for top of leaderboard)

    d2api/  (core app for creating/processing requests)for future   
      |-- utils.py  (the business logic, esp the api handler)    
      |-- constants.py  (parameters like secret keys, headers)   

    static/  (files used by everything)
      |-- bootstrap.min.css (cyborg custom bootstrap4 theme)
      |-- style.css (home-grown styles for the pages)

## Acknowledgments
Thanks to [Jessamyn Smith](https://www.codementor.io/jessamynsmith) at codementor who helped me navigate the Django labyrinth while making this project. Thanks to members of EC59 for general advice about the site, and to the Destiny2 developer community. Thanks to Bungie for making a great game and providing the API to developers.
