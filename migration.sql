CREATE TABLE campaign (
    social_network  VARCHAR(64)     NOT NULL,
    campaign_id     BIGINT,
    campaign_name   VARCHAR(2048)   NOT NULL,
    start_time      TIMESTAMP       NOT NULL,
    stop_time       TIMESTAMP       DEFAULT NULL,

    CONSTRAINT u_social_network_campaign
        UNIQUE (social_network, campaign_id)
);

CREATE TABLE advertising (
    social_network  VARCHAR(64)     NOT NULL,
    adv_id          BIGINT,
    adv_name        VARCHAR(1024)   DEFAULT NULL,
    adv_url         VARCHAR(1024)   DEFAULT NULL,
    adv_umt         JSONB           DEFAULT '{}',
    campaign_id     BIGINT          DEFAULT NULL,

    CONSTRAINT u_social_network_adv
        UNIQUE (social_network, adv_id)
);

CREATE TABLE statistics_day (
    social_network  VARCHAR(64)     NOT NULL,
    adv_id          BIGINT          NOT NULL,
    stat_date       DATE            DEFAULT CURRENT_DATE,
    spent           DECIMAL(12, 4)  DEFAULT 0,
    impressions     BIGINT          DEFAULT 0,
    clicks          BIGINT          DEFAULT 0,

    CONSTRAINT u_statistics_day
        UNIQUE (social_network, adv_id, stat_date)
);
