CREATE TABLE teams(
    teamId INT,
    owner VARCHAR(40) NOT NULL,
    teamName VARCHAR(40) NOT NULL,
    PRIMARY KEY(teamId)
);

CREATE TABLE years(
    teamId INT,
    year INT,
    wins INT,
    losses INT,
    pointsFor INT,
    finalStanding INT,
    rotWins INT,
    rotLosses INT,
    rotTies INT,
    PRIMARY KEY (teamId, year)
);

CREATE TABLE thisWeekSummary(
    week INT,
    year INT,
    topScorerId INT,
    lowScorerId INT,
    averageScore REAL,
    maxScore REAL,
    PRIMARY KEY (week, year)
);

-- CREATE TABLE thisWeekScores(
--     teamId INT,
--     weekId INT,
--     score INT
-- );