CREATE TABLE campaign (
    social_network VARCHAR(64) NOT NULL,
    campaign_id INT,
    campaign_name VARCHAR(2048) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    stop_time TIMESTAMP DEFAULT NULL,

    CONSTRAINT u_social_network_capmpaign
        UNIQUE (social_network, campagn_id)
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

CREATE TABLE ads_statistics (
    social_network  VARCHAR(64)     NOT NULL,
    adv_id          INT             NOT NULL,
    stat_date       TIMESTAMP,
    spent           DECIMAL(12, 4)  DEFAULT 0,
    impressions     INT             DEFAULT 0,
    clicks          INT             DEFAULT 0
);
