import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS bump_chart
        """,
        """ CREATE TABLE IF NOT EXISTS bump_chart (
                dimension CHAR(7),
                time SMALLINT NOT NULL,
                dimension_time VARCHAR(9),
                dimension_next_time VARCHAR(9),
                rank SMALLINT NOT NULL,
                next_rank SMALLINT NOT NULL,
                path_join BOOLEAN NOT NULL,
                measure FLOAT8 NOT NULL,
                actual_time CHAR(9)
                )
        """)
    conn = None
    try:
        # Read the connection parameters
        params = config()
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Create table one by one
        for command in commands:
            cur.execute(command)
        # Close communication with the PostgreSQL database server
        cur.close()
        # Commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# Run the create table function localy for testing.
if __name__ == '__main__':
    create_tables()
