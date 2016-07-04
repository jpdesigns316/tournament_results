#!/usr/bin/env python
#
# Test cases have been modified, or altered by Jonathan D. Peterson for
# improving test cases for tournament.py
#
# - Changed messages and displayed the outcome
# - Reformatted to be in compliant with Python coding standards
#
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these 
# test cases as appropriate to account for your module's added functionality.

from tournament import *


def test_count():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    delete_matches()
    delete_players()
    c = count_players()
    print "1. Confirmation on count_player() results"
    if c == '0':
        raise TypeError(
            "count_players should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, count_players should return zero.")
    register_player("Chandra Nalaar")
    c = count_players()
    if c != 1:
        raise ValueError(
        "One player registers, count_players() should be 1. Got {}".format(c))
    print "Results after one person has registered = {}".format(c)
    
    register_player("Jace Beleren")
    c = count_players()
    if c != 2:
        raise ValueError("After two players register, count_players() \
                         should be 2. Got {}".format(c))
    print "Results after two people have registered =  {}".format(c)
    
    delete_players()
    c = count_players()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "Results after tournament has been deleted = {}".format(c)


def test_standings_before_matches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    delete_matches()
    delete_players()
    register_player("Melpomene Murray")
    register_player("Randy Schwartz")
    print "2. Newly registered players appear in the standings with "
    print "no matches.\nDisplaying standings to confirm that no one "
    print "has a match."
    standings = player_standings()
    display_player_standings(standings)
    if len(standings) < 2:
        raise ValueError("Players should appear in player_standings even \
                         before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in \
                          standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each player_standings row should have four \
                        columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, 
                                matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in \
                         standings, even if they have no matches played.")
    
        
def test_report_matches():
    delete_matches()
    delete_players()
    register_player("Bruno Walton")
    register_player("Boots O'Neal")
    register_player("Cathy Burton")
    register_player("Diane Grant")
    print "3. Creating new tournament..."
    print "Displaying results after at beginning of tournament"
    standings = player_standings()
    display_player_standings(standings)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    [p1, p2, p3, p4] = [row[1] for row in standings]
    report_match(id1, id2)
    report_match(id3, id4)
    print "Match results"
    display_match_results(p1, p2)
    display_match_results(p3, p4)
    standings = player_standings()
    print "4. After a match, players have updated standings."
    display_player_standings(standings)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win \
                            recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins \
                              recorded.")
    
    
def test_reset_standings():
    print "5. After match deletion, player standings are properly reset, and"
    print "matches have been deleted.\nDislaying to confirm matches have been"
    print "reseted properly."
    delete_matches()
    standings = player_standings()
    display_player_standings(standings)

    
def test_pairings():
    """
    Test that pairings are generated properly both before and after match
    reporting.
    """
    test = []
    player = []
    player_id = []
    delete_matches()
    delete_players()
    register_player("Twilight Sparkle")
    register_player("Fluttershy")
    register_player("Applejack")
    register_player("Pinkie Pie")
    register_player("Michael Jordan")
    register_player("Peyton Manning")
    register_player("Wayne Gretzky")
    register_player("Jeff Gordon")
    print "6. After one match, players with one win are properly paired."
    standings = player_standings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    [pname1, pname2, pname3, pname4, 
     pname5, pname6, pname7, pname8] = [row[1] for row in standings]
    print "Round 1 Matches"
    pairings = swiss_pairings()
    display_pairings(pairings)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got \
            {pairs}".format(pairs=len(pairings)))
    report_match(id1, id2)
    display_match_results(pname1, pname2)
    report_match(id3, id4)
    display_match_results(pname3, pname4)
    report_match(id5, id6)
    display_match_results(pname5, pname6)
    report_match(id7, id8)
    display_match_results(pname7, pname8)
    pairings = swiss_pairings()
    print "Round 2 Matches"
    display_pairings(pairings)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got \
            {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset(
        [pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")


if __name__ == '__main__':
    print "--------------------BEGIN-TEST--------------------------"
    test_count()
    test_standings_before_matches()
    test_report_matches()
    test_reset_standings()
    test_pairings()
    print "Success!  All tests pass!"
