-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



-- Change to the admin to be able to delete an open database
-- Check to see if the database exise, if so delete it
-- Create a fresh database
-- Swich to tournament to add the table and views.
\c vagrant
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- Initialize the tournament players table
CREATE TABLE players  (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(25) NOT NULL
);

-- Initiazed the matches tables. This table is to keep track of wins and
-- losses throughout the tournament.
-- winner_id references the players.id
-- loser_id references the players.id
create table matches  (
    id serial primary key not null,
    winner_id INT,
    loser_id INT,
    FOREIGN KEY (winner_id) REFERENCES players(id),
    FOREIGN KEY (loser_id) REFERENCES players(id)
);


-- Gets the player's id and join it with the winners_id in the matches
-- table. It get the number of wins based on the number of times that 
-- player's id is in matches, and sets it to a column called wins.
-- Then sorts the table by the player's id in descending order.
CREATE MATERIALIZED VIEW v_player_wins AS
    SELECT players.id AS player, COUNT(matches.winner_id) AS wins
    FROM players LEFT JOIN matches
    ON players.id = matches.winner_id
    GROUP BY players.id, matches.winner_id
    ORDER BY players.id;

-- Gets the player's id and join it with the losers_id in the matches
-- table. It get the number of losses based on the number of times that 
-- player's id is in matches, and sets it to a column called losses.
-- Then sorts the table by the player's id in acending order.
CREATE MATERIALIZED VIEW v_player_losses AS
    SELECT players.id AS player, COUNT(matches.loser_id) AS losses
    FROM players LEFT JOIN matches
    ON players.id = matches.loser_id
    GROUP BY players.id, matches.loser_id
    ORDER BY players.id;
    
-- Generatate the number of matches that have neen played.
CREATE MATERIALIZED VIEW v_matches AS
    SELECT players.id AS player, count(matches) AS matches
    FROM players LEFT JOIN matches
    ON(players.id=matches.winner_id) OR(players.id=matches.loser_id)
    GROUP BY players.id
    ORDER BY players.id ASC;
