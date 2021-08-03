"""
This module takes care of extracting device interface configurations from json file & loads to database table.
"""

from contextlib import contextmanager
import json
from os  import getenv

import psycopg2


DB_NAME = "ztlmlrvh"
DB_USER = "ztlmlrvh"
DB_PASSWORD ="PqOzyyx3rBaU_CdWJpXnmib1QazLUdum"
DB_HOST = "chunee.db.elephantsql.com"
DB_PORT = "5432"

SQL_STATEMENT = """
    CREATE TABLE IF NOT EXISTS device_interface_config
    (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NULL,
    config JSON NOT NULL,
    port_channel_id INT  NULL,
    max_frame_size INT  NULL
    )"""

@contextmanager
def create_connection():
    """
    Creates a context manager to persist connection pooling and cursor, Returns a db connection object.
    """
    # conn = psycopg2.connect(database=getenv('DB_NAME'), user=getenv('DB_USER'),
    #                         password=getenv('DB_PASSWORD'), port=getenv('DB_PORT'), host=getenv('DB_HOST'))

    conn = psycopg2.connect( database=DB_NAME, user=DB_USER,
                             password=DB_PASSWORD, port=DB_PORT, host=DB_HOST )
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def create_table():
    """
    Given a SQL statement ,executes it after connecting to db.
    :return:connection
    """
    with create_connection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_STATEMENT)
        return conn


def process_data():
    """
    Process data and inserts to sql table.
    :param json_config:
    :return:
    """
    with open('configClear_v2.json') as config:
        json_config = json.load(config)
        cisco_ios_xe_native = json_config.get('frinx-uniconfig-topology:configuration').get('Cisco-IOS-XE-native:native')

        config_container = {
            "BDI" : cisco_ios_xe_native.get('interface').get('BDI'),
            "Loopback" : cisco_ios_xe_native.get('interface').get('Loopback'),
            "Port-channel" : cisco_ios_xe_native.get('interface').get('Port-channel'),
            "TenGigabitEthernet" : cisco_ios_xe_native.get('interface').get('TenGigabitEthernet'),
            "GigabitEthernet" : cisco_ios_xe_native.get( 'interface' ).get( 'GigabitEthernet' )
        }


    with create_connection() as conn:
        for k,v in config_container.items():
            for i in v:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO device_interface_config( name, description, config, port_channel_id, max_frame_size )
                VALUES( %s, %s, %s, %s, %s);
                """, (f"{k}{i.get('name')}",
                                  i.get('description'),
                                  json.dumps(i),
                                    i.get( 'Cisco-IOS-XE-ethernet:channel-group' ),
                                  i.get('mtu')
                                  )
                )


if __name__ == "__main__":
    create_table()
    process_data()
