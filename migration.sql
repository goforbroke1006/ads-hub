CREATE TABLE advertising (
    social_network VARCHAR(64) NOT NULL,
    project_id INT,
    exported_at TIMESTAMP NOT NULL,
    campagn_name VARCHAR(1024) NOT NULL,
    adv_id INT,
    adv_name VARCHAR(1024) DEFAULT NULL,
    adv_url VARCHAR(1024) DEFAULT NULL,
    adv_umt JSONB DEFAULT '{}',
    expenditure_per_day DECIMAL(12, 4) DEFAULT NULL,
    appearance_count INT DEFAULT 0,
    click_count INT DEFAULT 0,
    agent_id INT DEFAULT NULL
);
