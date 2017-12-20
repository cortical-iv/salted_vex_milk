# Salted Vex Milk
Processing clans in D2.

## Goal
Front page will have basic information about the clan (name, when it was formed, how many members, etc). There will be pages for clan leaderboards, individual clan member stats, including what each player is currently doing.  Allow for sorting by stats. Another page for links and content (link to ec59, to slack channel, youtube channel, strategy channels, etc).

## To do
### Get stub working with Clan model
- Push upsert logic into model or form rather than view.
- Functionalize the upsert operations, will be using a lot.
- GROUP_ID is acting as globals rather than getting passed. E.g., headers, base_url (in utils, and views, and forms: check on this). In views, clan_instance =  .... (clan_id=GROUP_ID). This seems smelly.
- Make sure logging is reasonable in view.
- Once Clan basic info is good, schedule it to update automatically once a night.

### Scale up infrastructure built for stub version
- Clan members
    - Basic information (name, id, etc)
    - Current activity
    - Stats
- May need to download and use the manifest.

### Make it look non-ugly
- Bootstrap it

## In ideal world
- Should work for multiple clans, so user can enter their clan id and get this information.
