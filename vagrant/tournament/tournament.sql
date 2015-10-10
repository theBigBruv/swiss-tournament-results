-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players ( player_id SERIAL PRIMARY KEY, name TEXT );

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	winner_id INTEGER REFERENCES players(player_id),
	loser_id INTEGER REFERENCES players(player_id),
	tied_player1_id INTEGER REFERENCES players(player_id),
	tied_player2_id INTEGER REFERENCES players(player_id)
);

-- Create view specifically for player wins
CREATE VIEW playerwins AS (
SELECT p.player_id, p.name, count(m.winner_id) AS wins
FROM players p
LEFT JOIN matches m
ON p.player_id=m.winner_id
GROUP BY p.player_id, p.name
ORDER BY count(m.winner_id) DESC
);

-- Create view specifically for player losses
CREATE VIEW playerlosses AS (
SELECT p.player_id, p.name, count(m.loser_id) AS losses
FROM players p
LEFT JOIN matches m
ON p.player_id=m.loser_id
GROUP BY p.player_id, p.name
ORDER BY count(m.loser_id) DESC
);

-- Create view specifically for player ties/draws
CREATE VIEW playerties AS (
SELECT p.player_id, p.name, count(m.tied_player1_id)+count(n.tied_player2_id) AS ties
FROM players p
LEFT JOIN matches m
ON p.player_id=m.tied_player1_id
LEFT JOIN matches n
ON p.player_id=n.tied_player2_id
GROUP BY p.player_id, p.name
ORDER BY count(m.tied_player1_id)+count(n.tied_player2_id) DESC
);

-- Combine views for wins, losses and ties/draws to create standings view
CREATE VIEW standings AS (
SELECT p.player_id, p.name, pw.wins AS wins, pt.ties AS ties, pw.wins+pl.losses+pt.ties AS matches_played
FROM players p
LEFT JOIN playerwins pw
ON p.player_id=pw.player_id
LEFT JOIN playerlosses pl
ON p.player_id=pl.player_id
LEFT JOIN playerties pt
ON p.player_id=pt.player_id
ORDER BY pw.wins DESC, pt.ties DESC
);
