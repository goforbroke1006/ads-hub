CREATE TABLE campaign (
    social_network VARCHAR(64) NOT NULL,
    campaign_id INT,
    campaign_name VARCHAR(2048) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP DEFAULT NULL,

    CONSTRAINT u_social_network_campaign
        UNIQUE (social_network, campaign_id)
);

CREATE TABLE advertising (
    social_network  VARCHAR(64) NOT NULL,
    adv_id          INT,
    adv_name        VARCHAR(1024) DEFAULT NULL,
    adv_url         VARCHAR(1024) DEFAULT NULL,
    adv_umt         JSONB DEFAULT '{}',
    campaign_id     INT DEFAULT NULL,

    CONSTRAINT u_social_network_adv
        UNIQUE (social_network, adv_id)
);

CREATE TABLE statistics_day (
    social_network  VARCHAR(64)     NOT NULL,
    adv_id          INT             NOT NULL,
    stat_date       DATE,
    spent           DECIMAL(12, 4)  DEFAULT 0,
    impressions     INT             DEFAULT 0,
    clicks          INT             DEFAULT 0,

    CONSTRAINT u_statistics_day
        UNIQUE (social_network, adv_id, stat_date)
);
