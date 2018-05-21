import datetime
import psycopg2


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

    def save_campaign(self, cam_id, name, start_time, stop_time):
        if isinstance(start_time, int):
            start_time = datetime.datetime.utcfromtimestamp(start_time)

        if isinstance(stop_time, int):
            stop_time = datetime.datetime.utcfromtimestamp(stop_time)

        start_time = start_time.strftime("%Y-%m-%d")
        stop_time = stop_time.strftime("%Y-%m-%d") if stop_time is not None else None

        campaign = self.get_campaign(cam_id)

        if campaign is not None:
            query = """
            UPDATE campaign
                SET 
                    campaign_name = %s,
                    start_time = %s, 
                    stop_time = %s
                WHERE social_network = %s AND campaign_id = %d;"""
            query = self.cursor.mogrify(
                query,
                (name, start_time, stop_time, self.social_network, cam_id)
            )
        else:
            query = "INSERT INTO campaign VALUES (%s, %s, %s, %s, %s);"
            query = self.cursor.mogrify(
                query,
                (self.social_network, cam_id, name, start_time, stop_time,)
            )

        if not self.debug_mode:
            print(query)

        self.cursor.execute(query)
        self.connection.commit()
        pass

    def get_campaign(self, campaign_id):
        query = "SELECT * FROM campaign " \
                "WHERE social_network = %s AND campaign_id = %s;"
        query = self.cursor.mogrify(query, (self.social_network, campaign_id,))

        if not self.debug_mode:
            print(query)

        result = self.cursor.execute(query)
        self.connection.commit()

        campaign = self.cursor.fetchone()
        return campaign
