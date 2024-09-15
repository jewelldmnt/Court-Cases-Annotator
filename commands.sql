-- SQLite
CREATE TABLE CourtCases (
    court_id INT NOT NULL,
    annotator VARCHAR(30),
    link TEXT,
    title TEXT, 
    whole_text TEXT,
    facts TEXT,
    issues TEXT,
    ruling TEXT,
    PRIMARY KEY(court_id)
)

CREATE TABLE IF NOT EXISTS CourtCases (
    court_id INT NOT NULL,
    annotator VARCHAR(30),
    link TEXT,
    title TEXT, 
    whole_text TEXT,
    facts TEXT,
    issues TEXT,
    ruling TEXT,
    PRIMARY KEY(court_id)
)

SELECT * FROM CourtCases;

SELECT COUNT(annotator), annotator FROM CourtCases GROUP BY annotator

DELETE FROM CourtCases;

DROP TABLE IF EXISTS CourtCases;

