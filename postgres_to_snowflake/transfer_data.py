import yaml
import logging
from os import getenv
import psycopg2 as pg
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from jinja2 import Template

logging.basicConfig(level='INFO')



class transfer_data(object):
    def __init__(self, config_file):
        self.config_file=config_file

    def load_file(self):
        with open(self.config_file, "r") as reader:
            config = yaml.load(reader)
        logging.info("system configuration from %s", self.config_file)
        return config

    def connect(self, connection_string):
        try:
            logging.info('Connecting to the PostgreSQL database...')
            conn = pg.connect(connection_string)
        except (Exception, pg.DatabaseError) as error:
            logging.error(error)
            if conn is not None:
                logging.info('Connection closed to PostgreSQL database...')
                conn.close()
        return conn

    def execute_query(self, conn, sql_query):
        try:
            logging.info('Executing sql query on PostgreSQL database...')
            cur = conn.cursor()
            # execute a statement
            logging.debug(sql_query)
            cur.execute(sql_query)
            result = cur.fetchall()
            logging.debug(result)

        except (Exception, pg.DatabaseError) as error:
            logging.error(error)
            # close the communication with the PostgreSQL
            cur.close()
        return result

    def copy_from_command(self, conn, copy_cmd, file_name):
        try:
            logging.info('Executing copy command on PostgreSQL database...')
            cur = conn.cursor()

            # execute a statement
            logging.debug(copy_cmd)
            with open(file_name, 'w') as f:
                cur.copy_expert(copy_cmd, f, size=8192)
            conn.commit()

        except (Exception, pg.DatabaseError) as error:
            logging.error(error)
            # close the communication with the PostgreSQL
            cur.close()

    def connect_to_snowflake(self):
        connection=None
        engine = create_engine(URL(
            account=getenv('account'),
            user=getenv('sf_username'),
            password=getenv('sf_password'),
            database=getenv('sf_database'),
            schema=getenv('sf_schema'),
            warehouse=getenv('sf_warehouse'),
            role='PUBLIC'
            )
        )
        try:
            connection = engine.connect()
        except(Exception) as error:
            if connection is not None:
                connection.close()
                engine.dispose()
        return connection

    def execute_query_snowflake_table(self, conn, sql_query):
        try:
            logging.info('Executing sql query on Snowflake database...')
            # execute a statement
            logging.debug(sql_query)
            results = conn.execute(sql_query)

            result = results.fetchall()
            logging.debug(result)

        except (Exception) as error:
            logging.error(error)
            # close the communication with the PostgreSQL
            conn.close()
        return result


    def get_queries_to_be_executed(self, yaml_file, system):
        for items in yaml_file['action']:
            if items['system'] == system:
                return items['query'].items()


    def get_tables_to_be_executed(self, yaml_file, system):
        for steps in yaml_file['action']:
            if steps['system'] == system:
                return steps['tables']


    def run_copy_command_on_ods(self, connection_object, yaml_file, system_key):
        #ODS extract
        for table_name, sql_query in self.get_queries_to_be_executed(yaml_file, system_key):
            connection_object=self.connect(connection_object)
            logging.info(f"{table_name} : {sql_query}")
            self.copy_from_command(connection_object,sql_query, f"{table_name}.csv")
            connection_object.close()

    def run_snowflake_query(self, yaml_file, system_key):
        #SnowFlake extract
        engine_conn = self.connect_to_snowflake()
        for table_name, sql_query in self.get_queries_to_be_executed(yaml_file, system_key):
            result = self.execute_query_snowflake_table(engine_conn, sql_query)
        engine_conn.close()

    def jinja_template(self, template_string, key_value):
        tm = Template(template_string)
        return tm.render(table=key_value)

    def run_queries_aganist_list_of_tables(self, connection_string, yaml_file):
        #jinja2 templatize query to be executed
        for table in self.get_tables_to_be_executed(yaml_file, 'tables'):
            for query_name, sql_query_template in self.get_queries_to_be_executed(yaml_file, 'select_query_ods'):
                connection_object = self.connect(connection_string)
                logging.info(f"{self.jinja_template(query_name, table)} : {self.jinja_template(sql_query_template, table)}")
                results=self.execute_query(connection_object, self.jinja_template(sql_query_template, table))
                for rows in results:
                    logging.info(f"results: {rows}")
                connection_object.close()



def main():
    td = transfer_data(config_file='config.yaml')
    td_load_yaml = td.load_file()
    generate_connection_string="user={0} password={1} host={2} port={3} dbname={4}".format(getenv('username'), getenv('password'), getenv('url'), getenv('port'), getenv('database'))

    #run queries aganist a list of tables
    td.run_queries_aganist_list_of_tables(generate_connection_string, td_load_yaml)

    #run copy command on ODS
    #td.run_copy_command_on_ods(generate_connection_string, td_load_yaml, 'ods')

    #run query on snowflake
    #td.run_snowflake_query(td_load_yaml, 'snowflake')



if __name__ == '__main__':
    main()

