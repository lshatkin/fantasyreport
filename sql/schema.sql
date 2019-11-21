CREATE TABLE teams(
    teamId INT,
    owner VARCHAR(40) NOT NULL,
    teamName VARCHAR(40) NOT NULL,
    PRIMARY KEY(teamId)
);

CREATE TABLE years(
    teamId INT,
    teamName VARCHAR(40),
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

CREATE TABLE yearSettings(
    year INT,
    regSeasonGames INT,
    playoffTeams INT,
    PRIMARY KEY (year)
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

CREATE TABLE historicalRosters(
    teamId INT,
    year INT,
    player1 VARCHAR(30),
    player1_pos VARCHAR(30),
    player1_team VARCHAR(30),
    player1_rank INT,
    player2 VARCHAR(30),
    player2_pos VARCHAR(30),
    player2_team VARCHAR(30),
    player2_rank INT,
    player3 VARCHAR(30),
    player3_pos VARCHAR(30),
    player3_team VARCHAR(30),
    player3_rank INT,
    player4 VARCHAR(30),
    player4_pos VARCHAR(30),
    player4_team VARCHAR(30),
    player4_rank INT,
    player5 VARCHAR(30),
    player5_pos VARCHAR(30),
    player5_team VARCHAR(30),
    player5_rank INT,
    player6 VARCHAR(30),
    player6_pos VARCHAR(30),
    player6_team VARCHAR(30),
    player6_rank INT,
    player7 VARCHAR(30),
    player7_pos VARCHAR(30),
    player7_team VARCHAR(30),
    player7_rank INT,
    player8 VARCHAR(30),
    player8_pos VARCHAR(30),
    player8_team VARCHAR(30),
    player8_rank INT,
    player9 VARCHAR(30),
    player9_pos VARCHAR(30),
    player9_team VARCHAR(30),
    player9_rank INT,
    player10 VARCHAR(30),
    player10_pos VARCHAR(30),
    player10_team VARCHAR(30),
    player10_rank INT,
    player11 VARCHAR(30),
    player11_pos VARCHAR(30),
    player11_team VARCHAR(30),
    player11_rank INT,
    player12 VARCHAR(30),
    player12_pos VARCHAR(30),
    player12_team VARCHAR(30),
    player12_rank INT,
    player13 VARCHAR(30),
    player13_pos VARCHAR(30),
    player13_team VARCHAR(30),
    player13_rank INT,
    player14 VARCHAR(30),
    player14_pos VARCHAR(30),
    player14_team VARCHAR(30),
    player14_rank INT,
    player15 VARCHAR(30),
    player15_pos VARCHAR(30),
    player15_team VARCHAR(30),
    player15_rank INT,
    player16 VARCHAR(30),
    player16_pos VARCHAR(30),
    player16_team VARCHAR(30),
    player16_rank INT,
    PRIMARY KEY(teamId, year)
);
