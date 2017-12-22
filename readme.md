# Salted Vex Milk
Processing clans in D2.

## Goal
Front page will have basic information about the clan. There will be pages for clan leaderboards, individual clan member stats, including what each player is currently doing.  Allow for sorting by stats. Another page for links and content (link to official clan site, to slack channel, youtube channel, strategy channels, etc).

## To do
### General
- Is it possible to develop on windows and linux machine?
- Push upsert logic into model or form rather than view. Functionalize it too.
- Automate updates: right now they are triggered by a button press (clan/member)
- logging is weird across multiple modules (utils and views): integrate settings into central module?

### Clan model
- GROUP_ID is acting as a global rather than getting passed. E.g., headers, base_url (in utils, and views, and forms: check on this). In views, clan_instance =  .... (clan_id=GROUP_ID). This seems smelly. In utils.extract_member_list:     
    clan = Clan.objects.get(clan_id = GROUP_ID)
also smelly.

### Member model
- What if user tries to update members if they haven't saved clan data yet? That will break this.
- has-Played_d2 causes timeout of requests :(
- D2 player?
- How would I automate this stuff when i have two different endpoints that are going into this (profile and get_members)
if GetProfile_res.json()['ErrorStatus'] == "DestinyAccountNotFound":
or 'ErrorCode' == 1601
    <they do not have a d2 account>
- constants.MEMBERSHIP_ENUM not being used, but should be probably for members view.
- Seems I should integrate this in but if there is a different endpoint for this how to best combine with the member-list endpoint?
- How to store date the membership list of the clan was updated? Maybe put that in clan? Seems to break modularity, but shouldn't those two be linked (e.g., clan has number of memberrs, and each member should be in db, no?)
- Give option of sorting alphabetically, join date, membership type, other info.
    - Current activity (there is an 'isOnline' in the get group member endpoint), or if not online, last login.
    - Stats
- Link in members.html to each member's page with all their stats.

### Scale up infrastructure built for stub version
- May need to download and use the manifest.

### Make it look non-ugly
- Bootstrap it

## In ideal world
- Should work for multiple clans, so user can enter their clan id and get this information.

## Things to remember
- When setting field (e.g., clan) in model (member) that is tethered to another model as foreign key (e.g., Member instance has Clan foreign key), you don't set the field to model instance, but to model_instance.id. Otherwise you end up in a world of hurt with errors like "That choice is not one of the available choices."
- Docs for sessions: http://docs.python-requests.org/en/master/api/#request-sessions
