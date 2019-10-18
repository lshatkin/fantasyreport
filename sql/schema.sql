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
    pointsFor REAL,
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
    minScore REAL,
    PRIMARY KEY (week, year)
);

CREATE TABLE thisWeekScores(
    teamId INT,
    score REAL,
    PRIMARY KEY (teamId)
);

CREATE TABLE players(
    name VARCHAR(40),
    points REAL,
    projection REAL,
    position VARCHAR(10),
    slot VARCHAR(10),
    team INT,
    PRIMARY KEY(name)
);
