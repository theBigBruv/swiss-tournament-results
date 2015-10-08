#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "select count(*) from players"
    c.execute(query)
    rows = c.fetchall()
    row = rows[0]
    count = int(row[0])
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = "select player_id, name, wins, ties, matches_played from standings"
    c.execute(query)
    rows = c.fetchall()
    standings = ([(int(row[0]), str(row[1]), int(row[2]), int(row[3]),
                 int(row[4])) for row in rows])
    db.close()

    return standings


# outcome included as an argument in this function in order to handle
# tie (draw) outcomes. winner and loser arguments also renamed
def reportMatch(outcome, winner_or_tie1, loser_or_tie2):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    # conditional statement that determnes what columns of table matches
    # to update based ob value of outcome variable
    if outcome == "winandloss":
        (c.execute("insert into matches (winner_id, loser_id) values (%s, %s)",
                   (winner_or_tie1, loser_or_tie2)))
    elif outcome == "tie":
        (c.execute("insert into matches (tied_player1_id, tied_player2_id)"
                   " values (%s, %s)", (winner_or_tie1, loser_or_tie2)))
    else:
        raise ValueError("Outcome can only be one of winandloss or tie.")
    db.commit()
    db.close()


def swissPairings():
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
    db = connect()
    c = db.cursor()
    query = "select player_id, name from standings"
    c.execute(query)
    rows = c.fetchall()

    pairings = []
    i = 0
    # loop that creates pairings based on ranked
    # players in the standings view
    while i < len(rows):
        pair = ((int(rows[i][0]), str(rows[i][1]),
                int(rows[i+1][0]), str(rows[i+1][1])))
        pairings.append(pair)

        i = i + 2

    db.close()

    return pairings


