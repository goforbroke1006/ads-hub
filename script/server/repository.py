import datetime
import psycopg2


CAMPAIGN_SELECT = """
SELECT 
    social_network,
    campaign_id,
    campaign_name,
    start_time,
    stop_time
FROM campaign 
WHERE 
    social_network = %s AND campaign_id = %s;
"""

CAMPAIGN_INSERT = """
INSERT INTO campaign (
    social_network,
    campaign_id,
    campaign_name,
    start_time,
    stop_time
) VALUES (%s, %s, %s, %s, %s);
"""

CAMPAIGN_UPDATE = """
UPDATE campaign
SET 
    campaign_name = %s, start_time = %s, stop_time = %s
WHERE
    social_network = %s AND campaign_id = %s;
"""


ADV_SELECT = """
SELECT 
    social_network,
    adv_id,
    adv_name,
    adv_url,
    adv_umt,
    campaign_id
FROM advertising 
WHERE 
    social_network = %s AND adv_id = %s;
"""

ADV_INSERT = """
INSERT INTO advertising (
    social_network, 
    adv_id, 
    adv_name, 
    adv_url, 
    campaign_id
) VALUES (%s, %s, %s, %s, %s);
            """

ADV_UPDATE = """
UPDATE advertising
SET
    adv_name = %s,
    adv_url = %s,
    campaign_id = %s
WHERE social_network = %s AND adv_id = %s;
"""


STAT_SELECT = """
SELECT social_network, adv_id, stat_date, spent, impressions, clicks
FROM statistics_day
WHERE 
    social_network = %s 
    AND adv_id = %s
    AND stat_date = %s;
"""

STAT_INSERT = """
INSERT INTO statistics_day (
    social_network, adv_id, stat_date,
    spent, impressions, clicks
) VALUES (
    %s, %s, %s, 
    %s, %s, %s
);
"""

STAT_UPDATE = """
UPDATE statistics_day
SET
    spent = %s, impressions = %s, clicks = %s
WHERE 
    social_network = %s AND adv_id = %s AND stat_date = %s
"""


class AdsRepository:

    def __init__(self, params, social_network, debug_mode=False):
        self.connection = self.connect(params)
        self.cursor = self.connection.cursor()
        self.social_network = social_network
        self.debug_mode = debug_mode
        pass

    @staticmethod
    def connect(params):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return conn

    def get_campaign(self, campaign_id):
        query = self.cursor.mogrify(CAMPAIGN_SELECT, (
            self.social_network, campaign_id,
        ))

        if self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()

        campaign = self.cursor.fetchone()
        return campaign

    def save_campaign(self, cam_id, name, start_time, stop_time):
        if isinstance(start_time, int):
            start_time = datetime.datetime.utcfromtimestamp(start_time)

        if isinstance(stop_time, int):
            stop_time = datetime.datetime.utcfromtimestamp(stop_time)

        start_time = start_time.strftime("%Y-%m-%d")
        stop_time = stop_time.strftime("%Y-%m-%d") \
            if stop_time is not None else None

        campaign = self.get_campaign(cam_id)

        if campaign is not None:
            query = self.cursor.mogrify(CAMPAIGN_UPDATE, (
                name, start_time, stop_time, self.social_network, cam_id
            ))
        else:
            query = self.cursor.mogrify(CAMPAIGN_INSERT, (
                self.social_network, cam_id, name, start_time, stop_time,
            ))

        if self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()
        pass

    def get_advertising(self, adv_id):
        query = self.cursor.mogrify(ADV_SELECT, (
            self.social_network, adv_id,
        ))

        if self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()

        adv = self.cursor.fetchone()
        return adv

    def save_advertising(self, adv_id, adv_name, adv_url, campaign_id, umt=None):
        if umt is None:
            umt = {}

        adv = self.get_advertising(adv_id)
        if adv is not None:
            query = self.cursor.mogrify(ADV_UPDATE, (
                adv_name, adv_url, campaign_id,
                self.social_network, adv_id
            ))
        else:
            query = self.cursor.mogrify(ADV_INSERT, (
                self.social_network, adv_id, adv_name, adv_url, campaign_id,
            ))

        if self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()
        pass

    def get_statistics_day(self, adv_id, stat_date):
        if not isinstance(stat_date, datetime.date):
            raise Exception("stat_day should be date")

        query = self.cursor.mogrify(STAT_SELECT, (
            self.social_network, adv_id, stat_date,
        ))

        if self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()

        stat = self.cursor.fetchone()
        return stat

    def save_statistics_day(self, adv_id, stat_date, spent, impressions, clicks):
        stat = self.get_statistics_day(adv_id, stat_date)
        if stat is not None:
            query = self.cursor.mogrify(STAT_UPDATE, (
                spent, impressions, clicks,
                self.social_network, adv_id, stat_date,
            ))
        else:
            query = self.cursor.mogrify(STAT_INSERT, (
                self.social_network, adv_id, stat_date,
                spent, impressions, clicks,
            ))

        if self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()
        pass
