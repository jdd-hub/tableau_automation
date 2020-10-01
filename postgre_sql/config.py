from configparser import ConfigParser

"""
Connection parameters:
----------------------

database: the name of the database that you want to connect.
user: the username used to authenticate.
password: password used to authenticate.
host: database server address e.g., localhost or an IP address.
port: the port number that defaults to 5432 if it is not provided.

"""


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


if __name__ == '__main__':
    print(config())