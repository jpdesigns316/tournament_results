#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
#  Additions written by: Jonathan D. Peterson
#
#  Credit
#  swiss_pairing code was written with help from GitHub repo: 
#  https://github.com/allanbreyes/udacity-full-stack.git
#  - Added commenting and made logical variable names
#
#  Code reviewer
#  Reminded me to use try-catch (sorry I think more Java) 
#  statements, and to fall back on the things I already 
#  should know and not make repetative code.


import psycopg2


def connect(dbname='tournament'):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=%s" % dbname)
        cursor = db.cursor()
        return db, cursor
    except:
        IOError('Error connecting to database %s' % db)


def commit_query(query):
    """Connects, sends query, executes, commits, and closes.
    Returns the databse object."""
    db, cursor = connect()
    cursor.execute(query)
    db.commit()
    db.close()
    return db


def delete_matches():
    """Remove all the match records from the database."""
    query = "DELETE from matches WHERE id NOTNULL;"
    commit_query(query)
    refresh_views()



def delete_players():
    """Remove all the player records from the database."""
    query = "DELETE from players WHERE id NOTNULL;"
    commit_query(query)
    refresh_views()


def count_players():
    """Returns the number of players currently registered."""
    query = """
    SELECT COUNT(id) from players;
    """
    db, cursor = connect()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    print result
    return int(result)


def register_player(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.
    Args:
      name: the player's full name (need not be unique).
    """
    query = """
    INSERT INTO players (name) VALUES (%s)
    """
    db, cursor = connect()
    cursor.execute(query, (name,))
    db.commit()
    db.close()


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    refresh_views()
    query = """
    SELECT players.id, players.name, v_player_wins.wins, v_matches.matches
    FROM players
    LEFT JOIN v_player_wins ON players.id = v_player_wins.player
    LEFT JOIN v_matches ON players.id = v_matches.player
    GROUP BY players.id, players.name, v_player_wins.wins, v_matches.matches
    ORDER BY v_player_wins.wins DESC;
	"""
    db, cursor = connect()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def report_match(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = """
    INSERT INTO matches (winner_id, loser_id)
    VALUES (%s, %s)
    """ 
    db, cursor = connect()
    cursor.execute(query, (int(winner), int(loser)))
    db.commit()
    db.close()
    refresh_views()


def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Put the id and name into standings.
    standings = [(record[0], record[1]) for record in player_standings()]
    if len(standings) < 2:
        raise KeyError("Not enough players.")
    ids = standings[0::2]  # Put the winners in a list using slicing
    players = standings[1::2]  # Put the losers in a list using slicing
    pairings = zip(ids, players)  # Merges the id's annd player into one list

    # Create a list merging the pairs together
    results = [tuple(list(sum(pairing, ()))) for pairing in pairings]

    return results

# Additional methods to show information and to confirm the results.


    
    

def display_match_results(winner, loser):
    """
    Displays the winner of the match in a format who which player wins.
    """
    print "{winner} beats {loser}".format(winner=winner, loser=loser)


def display_player_standings(lst):
    """
    Displays the the standing of the players.
    """
    print "{name:22}{w:3}{l:3} {matches:3}".format(name='Name',
                                                   w='W',
                                                   l='L',
                                                   matches='Matches')
    for name in lst:
        print "{name:20}{w:3}{l:3} {matches:3}".format(name=name[1],
                                                       w=name[2],
                                                       l=name[3]-name[2],
                                                       matches=name[3])


def display_pairings(lst):
    """
    Will give a list of matches so players know who they are going to be
    playing against.
    """
    for row in range(0, len(lst)):
        print "{pid:4} {pname:20} {oid} {oname}".format(pid=lst[row][0],
                                                        pname=lst[row][1],
                                                        oid=lst[row][2],
                                                        oname=lst[row][3])

def refresh_views():
    """Refreshes materialized views derived from MATCHES."""
    commit_query("REFRESH MATERIALIZED VIEW v_player_wins;")
    commit_query("REFRESH MATERIALIZED VIEW v_player_losses;")
    commit_query("REFRESH MATERIALIZED VIEW v_matches;")

