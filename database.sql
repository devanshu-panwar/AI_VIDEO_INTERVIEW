-- =====================================================
-- DATABASE INITIALIZATION
-- =====================================================

-- Create database (run only once)
CREATE DATABASE video_interview_db;

-- Switch to it
\c video_interview_db;

-- =====================================================
-- USERS TABLE
-- =====================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    skill VARCHAR(255),
    job_role VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type VARCHAR(100) NOT NULL,
    task_id VARCHAR(200) NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =====================================================
-- TECHNICAL ROUND QUESTIONS
-- =====================================================
CREATE TABLE technical_round (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT,
    skill VARCHAR(255),
    difficulty VARCHAR(50)
);

-- =====================================================
-- HR ROUND QUESTIONS
-- =====================================================
CREATE TABLE hr_round (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL
);

-- =====================================================
-- CULTURAL FIT QUESTIONS
-- =====================================================
CREATE TABLE cultural_fit (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL
);

-- =====================================================
-- TECHNICAL RESPONSES
-- =====================================================
CREATE TABLE technical_round_response (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_id VARCHAR NOT NULL,
    question_id INTEGER NOT NULL,
    transcript TEXT NOT NULL,

    -- Foreign Keys
    CONSTRAINT fk_tech_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT fk_tech_question
        FOREIGN KEY (question_id) REFERENCES technical_round(id)
);


-- =====================================================
-- HR ROUND RESPONSES
-- =====================================================
CREATE TABLE hr_round_response (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_id VARCHAR NOT NULL,
    question_id INTEGER NOT NULL,
    transcript TEXT NOT NULL,

    -- Foreign Keys
    CONSTRAINT fk_hr_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT fk_hr_question
        FOREIGN KEY (question_id) REFERENCES hr_round(id)
);


-- =====================================================
-- CULTURAL FIT RESPONSES
-- =====================================================
CREATE TABLE cultural_round_response (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_id VARCHAR NOT NULL,
    question_id INTEGER NOT NULL,
    transcript TEXT NOT NULL,

    -- Foreign Keys
    CONSTRAINT fk_cultural_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT fk_cultural_question
        FOREIGN KEY (question_id) REFERENCES cultural_fit(id)
);


-- =====================================================
-- OPTIONAL: RELATIONSHIPS (not enforced, but logical)
-- =====================================================
-- Each response is tied to a user via task_id
-- This ensures we can trace interviews to candidates
-- You can add a foreign key if you want strict linkage:
--
-- ALTER TABLE responses
-- ADD CONSTRAINT fk_responses_user
-- FOREIGN KEY (task_id) REFERENCES users(task_id)
-- ON DELETE CASCADE;

-- =====================================================
-- SAMPLE DATA (OPTIONAL)
-- =====================================================

-- HR round sample questions
INSERT INTO hr_round (question_text) VALUES
('Tell me about yourself.'),
('What are your strengths and weaknesses?'),
('Why should we hire you?');

-- Technical sample questions
INSERT INTO technical_round (question, answer, skill, difficulty) VALUES
('What is Python?', 'Python is a high-level, interpreted programming language.', 'Python', 'Easy'),
('Explain OOP concepts.', 'OOP stands for Object-Oriented Programming and includes Encapsulation, Inheritance, Polymorphism, and Abstraction.', 'OOP', 'Medium'),
('What is a database index?', 'An index speeds up data retrieval in a database table.', 'Database', 'Medium');

-- Cultural fit questions
INSERT INTO cultural_fit (question_text) VALUES
('Describe your ideal work environment.'),
('How do you handle conflicts with team members?'),
('What motivates you at work?');

-- =====================================================
-- CHECK TABLES
-- =====================================================
-- \dt   -- List tables
-- \d users  -- Describe a table
