# Tournament Results

This is fourth project in which I had completed for my Udacity nanodegree. The purpose of this
project is to be able to learn and understand SQL and how it can work within the Python
environment. Though Python does modules for sqlite, this project it was required to
use Postgres. This was because the features that it included.

## Installation

**Needed to run**
[Vagrant] (http://www.vagrantup.com/)
[VirtualBox] (https://www.virtualbox.org/)

**Step One**

If you already have a virtual machine installed skip to step to, if not
download it and install it with the link above

**Step Two**

Install Vagrant.

**Step Three**
Clone or git this repository (To be added after meeting specifications) and
install it to a directory called fullstack

**Step Four**

```
cd fullstack
vagrant up
vagrant ssh
```

**Set Five**

Once in the VM type:
```
$ cd /vagrant/tournament
$ psql tournament < tournament.sql
$ python tournament_test.py
```

## Methods

**connect(dbname=DBNAME)**
This is the method that you use to connect to the database. If you do not want to use the default one
just type the name of the database you want to connect to.

**commit_query(query, dbname=DBNAME)**
Method used to commit the querys to the default database, or the name you want to commit the query to

**delete_matches()**
Deletes the matches from the tournament
    
**delete_players()**
Deletes players from the tournament

**count_players()**
Counts the number of players in the tournament

**register_player(name)**
Adds name to the tournament
    
**player_standings()**
Creates the list for the player_standing.

**report_match(winner, loser)**
Adds the winner and loser to the matches table to be used to help generate the standings.

**swiss_pairings()**
Pairs players together base on the [Swiss Pairing] (https://en.wikipedia.org/wiki/Swiss-system_tournament).

**display_match_results(winner, loser)**
Visuals show the winner and loser of the match.
```
Peyton Manning beats Tom Brady
```

**display_player_standings(lst)**
Display the standings based in the tournament.
lst should be the name of the list created by player_standings()
```
Matches             W   L   Matches
Peyton Manning      1   0   1
Cam Newton          1   0   1
Tom Brady           0   1   1
Philip Rives        0   1   1
```

**display_pairings(lst)**
Displays the players who will be playing against each other.
_lst_ should be the name of the list created by player_standings()
```
1 Peyton Manning     4 Cam Newton
2 Tom Brady          3 Philip Rivers
```

## SQL Formating
**players**
This is the player's database which will house the player's id and their name

**match**
This database will keep track of the wins and losses. It will store the winners
or losers id, which then will be used in views and querys to get the numeric
values of those.

**v_player_wins**
A view created to keep track of the number of times a player's id is in the
winner_id in the matches database.

**v_player_losses**
A view created to keep track of the number of times a player's id is in the
loser_id in the matches database.

**v_matches**
A view created to keep track of the number of matches a player had played 
base on the number of wins and losses a player has.

