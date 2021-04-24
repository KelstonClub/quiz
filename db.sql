CREATE TABLE IF NOT EXISTS quizzes (
	id INTEGER PRIMARY KEY NOT NULL,
	name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
	id INTEGER PRIMARY KEY NOT NULL,
	quiz_id INTEGER NOT NULL,
	text TEXT NOT NULL,
	type VARCHAR NOT NULL,

	FOREIGN KEY(quiz_id) REFERENCES quiz(id)
);

CREATE TABLE IF NOT EXISTS answers (
	id INTEGER PRIMARY KEY,
	question_id INT NOT NULL,
	text TEXT NULL,
	is_right BOOL NOT NULL DEFAULT false,
	
	FOREIGN KEY(question_id) REFERENCES questions(id)
);
