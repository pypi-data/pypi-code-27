#!/usr/bin/env python

import logging
import abc
from .aws import Redshift
from .extras import get_epoch_timestamp, get_business_regions
from .file import JSONFile


class Hydra(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, brand, channel, rdl_schema, odl_schema):
        """
        Constructor
        :param brand: brand name OLX or Letgo [String]
        :param channel: channel name: Android, iOS or Web [String]
        :param rdl_schema: raw data layer schema [String]
        :param odl_schema: operation data layer schema [String]
        """
        # common attributes
        self._logger = logging.getLogger(__name__)
        self._rdl_schema = rdl_schema
        self._odl_schema = odl_schema
        self._brand = brand.lower()
        self._channel = channel.lower()
        self._epoch = get_epoch_timestamp
        self._rdl_tables_views = {}

        # ODL tables/views
        self._odl_tables_views = {}
        for business_region in get_business_regions():
            odl_table_prefix = 'panamera{brand}_{business_region}_hydra_ninja_{channel}'.format(brand=self._brand,
                                                                                                business_region=business_region,
                                                                                                channel=self._channel)
            self._odl_tables_views[business_region] = {'prefix': odl_table_prefix,
                                                       'template_table': '{odl_schema}.{odl_table_prefix}_template'.format(odl_schema=self._odl_schema,
                                                                                                                           odl_table_prefix=odl_table_prefix),
                                                       'hourly_table': '{odl_schema}.fact_{brand}_{business_region}_hydra_hourly_{channel}'.format(odl_schema=self._odl_schema,
                                                                                                                                                   brand=self._brand,
                                                                                                                                                   business_region=business_region,
                                                                                                                                                   channel=channel),
                                                       'transformation_view': '{odl_schema}.{odl_table_prefix}_transformation_view'.format(odl_schema=self._odl_schema,
                                                                                                                                           odl_table_prefix=odl_table_prefix),
                                                       'hourly_transformation_view': '{odl_schema}.{odl_table_prefix}_hourly_transformation_view'.format(odl_schema=self._odl_schema,
                                                                                                                                                         odl_table_prefix=odl_table_prefix)
                                                       }

        self._logger.debug(self._odl_tables_views)

        # database
        self._db_client = None

        # flags
        self._rdl_sync_table_truncated = False
        self._rdl_staging_table_truncated = False
        self._rdl_staging_table_loaded = False

        # files loaded/failed
        self._total_rows_affected = 0
        self._total_files_processed = 0
        self._ok_files = []
        self._ko_files = []

    def connect_database(self, config, profile, arn):
        """
        Configure database connection
        :param config: database configuration file path [String]
        :param profile: profile to connect to database [String]
        :param arn: role used to copy data from S3 to Redshift [String]
        :return: None
        """
        try:
            db_config = JSONFile(config)
            db_config.load()
            db_settings = db_config.get(profile)
            self._logger.info("Loaded database configuration file '{config}'.".format(config=config))
            self._db_client = Redshift(**db_settings)
            self._db_client.set_credentials(arn)
            self._logger.info("Connected")

        except Exception as e:
            self._logger.error(repr(e))
            raise

    @abc.abstractmethod
    def extract(self, s3_path, json_as):
        """
        Extract data from the S3 and copy it to the sync table
        :param s3_path: s3 path to json file to load [String]
        :param json_as: s3 path to json manifest or 'auto' option [String]
        :return: None
        """
        return

    @abc.abstractmethod
    def transform(self):
        """
        Transform data loaded in the sync table and insert it in the staging table (RDL)
        :return: None
        """
        return

    def load(self):
        """
        Load data into the final table from the staging table [ODL]
        :return: None
        """
        return


class PanameraStream(Hydra):
    def __init__(self, brand, channel, rdl_schema, odl_schema):
        """
        Constructor
        :param brand: brand name OLX or Letgo [String]
        :param channel: channel name: Android, iOS or Web [String]
        :param rdl_schema: raw data layer schema [String]
        :param odl_schema: operation data layer schema [String]
        """
        # super initialization
        Hydra.__init__(self, brand, channel, rdl_schema, odl_schema)

        # logger
        self._logger = logging.getLogger(__name__)

        # region
        self._region = None

        # RDL tables/views
        rdl_table_prefix = 'panamera{brand}_ninja_{channel}'.format(brand=self._brand,
                                                                    channel=channel)

        self._rdl_tables_views = {'prefix': rdl_table_prefix,
                                  'sync_table': '{rdl_schema}.{rdl_table_prefix}_sync'.format(rdl_schema=self._rdl_schema,
                                                                                              rdl_table_prefix=rdl_table_prefix),
                                  'staging_table': '{rdl_schema}.{rdl_table_prefix}_staging'.format(rdl_schema=self._rdl_schema,
                                                                                                    rdl_table_prefix=rdl_table_prefix),
                                  'transformation_view': '{rdl_schema}.{rdl_table_prefix}_transformation_view'.format(rdl_schema=self._rdl_schema,
                                                                                                                      rdl_table_prefix=rdl_table_prefix)
                                  }

        self._logger.debug(self._rdl_tables_views)

    def extract(self, s3_path, json_as):
        """
        Extract data from the S3 and copy it to the sync table
        :param s3_path: s3 path to json file to load [String]
        :param json_as: s3 path to json manifest or 'auto' option [String]
        :return: None
        """
        try:
            if self._db_client:
                if not self._rdl_sync_table_truncated:
                    self._db_client.truncate(self._rdl_tables_views['sync_table'])
                    self._logger.info("TRUNCATE completed in the sync table '{sync_table}'.".format(sync_table=self._rdl_tables_views['sync_table']))
                    self._rdl_sync_table_truncated = True

                result = self._db_client.copy(prefix=s3_path,
                                              table=self._rdl_tables_views['sync_table'],
                                              jsonas=json_as,
                                              compression='GZIP',
                                              maxerror=100000,
                                              truncatecolumns=True,
                                              acceptanydate=True,
                                              acceptinvchars=True,
                                              compupdate=False,
                                              statupdate=False)

                self._logger.info("COPY of the path '{s3_path}' completed' [Rows: {rows}]".format(s3_path=s3_path,
                                                                                                  rows=result['rowcount']))
                self._total_rows_affected += result['rowcount']
                self._ok_files.append(s3_path)
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._ko_files.append(s3_path)
            self._logger.error("Could not load the path '{s3_path}' into the table '{sync_table}', skipping loading. [{error}]".format(s3_path=s3_path,
                                                                                                                                       sync_table=self._rdl_tables_views['sync_table'],
                                                                                                                                       error=e.message))
            pass

        self._total_files_processed += 1

    def transform(self):
        """
        Transform data loaded in the sync table and insert it in the staging table (RDL)
        :return: None
        """
        try:
            if self._db_client:
                if self._total_rows_affected > 0:
                    # truncate staging table
                    self._db_client.truncate(self._rdl_tables_views['staging_table'])
                    self._logger.info("TRUNCATE completed in the staging table '{staging_table}'.".format(staging_table=self._rdl_tables_views['staging_table']))

                    # transform and insert data into staging table using transformation view
                    query = 'INSERT INTO {staging_table} SELECT * FROM {transformation_view};'.format(staging_table=self._rdl_tables_views['staging_table'],
                                                                                                      transformation_view=self._rdl_tables_views['transformation_view'])
                    result = self._db_client.execute(query)
                    self._logger.info("INSERT completed in the staging table '{staging_table}' [Rows: {rows}]".format(staging_table=self._rdl_tables_views['staging_table'],
                                                                                                                      rows=result['rowcount']))
                    if result['rowcount'] > 0:
                        self._rdl_staging_table_loaded = True
                        self._db_client.analyze(self._rdl_tables_views['staging_table'])

                else:
                    # checking why the the totals rows is equal to zero
                    if self._rdl_sync_table_truncated:
                        if len(self._ko_files) == self._total_files_processed:
                            extra_message = 'Check files, seems they are invalid or have any error.'
                        elif len(self._ok_files) == self._total_files_processed:
                            extra_message = 'Check files, seems they are empty.'
                        else:
                            extra_message = 'Check files, seems they are invalid/empty or have any error.'
                    else:
                        extra_message = 'Execute extract method to load it.'
                    raise Exception("Sync table '{sync_table}' is empty. {extra_message}".format(sync_table=self._rdl_tables_views['sync_table'],
                                                                                                 extra_message=extra_message))
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise

    def load(self):
        """
        Load data into the final table from the staging table [ODL]
        :return: None
        """
        try:
            if self._db_client:
                if self._rdl_staging_table_loaded:
                    # getting business region with data loaded
                    query = """SELECT DISTINCT 
                                    business_region     AS region,
                                    COUNT(*)            AS rowcount
                               FROM {staging_table} 
                               ORDER BY business_region;
                            """.format(staging_table=self._rdl_tables_views['staging_table'])

                    result = self._db_client.execute(query)
                    regions_with_data = result['data']

                    for row in regions_with_data:
                        if row.region == 'unknown':
                            self._logger.warning("Rows with 'unknown' business region will not moved to the hourly/tracking tables [Rows: {rows}]".format(rows=row.rowcount))
                        else:
                            # creating staging table
                            staging_table = self._odl_tables_views[row.region]['prefix'] + '_{epoch}_staging'.format(epoch=get_epoch_timestamp())
                            query = 'CREATE TEMP TABLE {staging_table} (LIKE: {template_table});'.format(staging_table=staging_table,
                                                                                                         template_table=self._odl_tables_views[row.region]['template_table'])

                            self._db_client.execute(query)
                            self._logger.debug("CREATE TEMP table '{staging_table}' completed.".format(staging_table=staging_table))

                            # inserting data into TEMP table
                            query = """
                                    INSERT INTO {staging_table}
                                    SELECT * FROM {transformation_view}
                                    WHERE business_region = '{region}';
                                    """.format(staging_table=staging_table,
                                               transformation_view=self._odl_tables_views[row.region]['transformation_view'],
                                               region=row.region)

                            result = self._db_client.execute(query)

                            if result['rowcount'] > 0:
                                self._logger.info("INSERT INTO TEMP table '{staging_table}' completed [Rows: {rows}]".format(staging_table=staging_table,
                                                                                                                             rows=result['rowcount']))
                                # deleting data in hourly table
                                query = """
                                        DELETE FROM {hourly_table}
                                        USING (SELECT DISTINCT 
                                                    server_path                                                  AS server_path,
                                                    SPLIT_PART(country_sk,'|',1) || split_part(country_sk,'|',3) AS livesync_dbname,
                                                    TO_CHAR(time_event_local, 'YYYYMMDDHH24')::INTEGER           AS hour_sk
                                        FROM  {staging_table}) AS tmp
                                        WHERE {hourly_table}.server_path = tmp.server_path
                                        AND   {hourly_table}.livesync_dbname = tmp.livesync_dbname
                                        AND   {hourly_table}.hour_sk = tmp.hour_sk;
                                        """.format(hourly_table=self._odl_tables_views[row.region]['hourly_table'],
                                                   staging_table=staging_table)

                                result = self._db_client.execute(query)
                                self._logger.info("DELETE of data from hourly table '{hourly_table}' completed [Rows: {rows}]".format(hourly_table=self._odl_tables_views[row.region]['hourly_table'],
                                                                                                                                      rows=result['rowcount']))

                                # inserting data in hourly table
                                query = 'INSERT INTO {hourly_table} SELECT * FROM {staging_table};'.format(hourly_table=self._odl_tables_views[row.region]['hourly_table'],
                                                                                                           staging_table=staging_table)

                                result = self._db_client.execute(query)
                                self._logger.info("INSERT INTO TEMP table '{hourly_table}' completed [Rows: {rows}]".format(hourly_table=self._odl_tables_views[row.region]['hourly_table'],
                                                                                                                            rows=result['rowcount']))

                                # selecting distinct months to load
                                query = """
                                        SELECT DISTINCT
                                            TO_CHAR(date_event_nk, 'YYYYMM') AS month_nk
                                        FROM {staging_table}
                                        WHERE date_event_nk IS NOT NULL;
                                        """.format(staging_table=staging_table)

                                result = self._db_client.execute(query)
                                months = result['data']

                                for month in months:
                                    # creating final table if does not exist
                                    tracking_table = self._odl_schema + '.' + self._odl_tables_views[row.region]['prefix'] + '_' + month
                                    query = 'CREATE TABLE IF NOT EXISTS {tracking_table} (LIKE: {template_table});'.format(tracking_table=tracking_table,
                                                                                                                           template_table=self._odl_tables_views[row.region]['template_table'])

                                    self._db_client.execute(query)
                                    self._logger.debug("CREATE table '{tracking_table}' completed.".format(tracking_table=tracking_table))

                                    # deleting data in tracking table
                                    query = """
                                        DELETE FROM {tracking_table}
                                        USING (SELECT DISTINCT 
                                                    server_path             AS server_path,
                                                    country_sk              AS country_sk,
                                                    min(time_event_local)   AS min_time_event_local,
                                                    max(time_event_local)   AS max_time_event_local
                                        FROM  {staging_table}) AS tmp
                                        WHERE {tracking_table}.server_path = tmp.server_path
                                        AND   {tracking_table}.country_sk = tmp.country_sk
                                        AND   {tracking_table}.time_event_local BETWEEN tmp.min_time_event_local AND tmp.max_time_event_local;
                                        """.format(tracking_table=tracking_table,
                                                   staging_table=staging_table)

                                    result = self._db_client.execute(query)
                                    self._logger.info("DELETE of data from tracking table '{tracking_table}' completed [Rows: {rows}]".format(tracking_table=tracking_table,
                                                                                                                                              rows=result['rowcount']))
                                    # inserting data in tracking table
                                    query = 'INSERT INTO {tracking_table} SELECT * FROM {staging_table};'.format(tracking_table=tracking_table,
                                                                                                                 staging_table=staging_table)

                                    result = self._db_client.execute(query)
                                    self._logger.info("INSERT INTO table '{tracking_table}' completed [Rows: {rows}]".format(tracking_table=tracking_table,
                                                                                                                             rows=result['rows']))

                                    # drop staging table
                                    self._db_client.drop(staging_table)
                            else:
                                self._logger.warning("No data loaded in TEMP table '{staging_table}'".format(staging_table=staging_table))

                            self._db_client.drop(staging_table)

                else:
                    if self._rdl_staging_table_truncated:
                        raise Exception("Staging table '{staging_table}' is empty.".format(staging_table=self._rdl_tables_views['staging_table']))
                    else:
                        raise Exception("Staging table '{staging_table}' was not loaded.".format(staging_table=self._rdl_tables_views['staging_table']))
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise


class LegacyStream(Hydra):
    def __init__(self, brand, channel, rdl_schema, odl_schema):
        """
        Constructor
        :param brand: brand name OLX or Letgo [String]
        :param channel: channel name: Android, iOS or Web [String]
        :param rdl_schema: raw data layer schema [String]
        :param odl_schema: operation data layer schema [String]
        """
        # super initialization
        Hydra.__init__(self, brand, channel, rdl_schema, odl_schema)

        # logger
        self._logger = logging.getLogger(__name__)

        # region
        self._region = None

        # RDL tables/views
        rdl_table_prefix = 'panamera{brand}_ninja_{channel}'.format(brand=self._brand,
                                                                    channel=channel)

        self._rdl_tables_views = {'prefix': rdl_table_prefix,
                                  'sync_table': '{rdl_schema}.{rdl_table_prefix}_sync'.format(rdl_schema=self._rdl_schema,
                                                                                              rdl_table_prefix=rdl_table_prefix),
                                  'staging_table': '{rdl_schema}.{rdl_table_prefix}_staging'.format(rdl_schema=self._rdl_schema,
                                                                                                    rdl_table_prefix=rdl_table_prefix),
                                  'transformation_view': '{rdl_schema}.{rdl_table_prefix}_transformation_view'.format(rdl_schema=self._rdl_schema,
                                                                                                                      rdl_table_prefix=rdl_table_prefix)
                                  }

        self._logger.debug(self._rdl_tables_views)

    def extract(self, s3_path, json_as):
        """
        Extract data from the S3 and copy it to the sync table
        :param s3_path: s3 path to json file to load [String]
        :param json_as: s3 path to json manifest or 'auto' option [String]
        :return: None
        """
        try:
            if self._db_client:
                if not self._rdl_sync_table_truncated:
                    self._db_client.truncate(self._rdl_tables_views['sync_table'])
                    self._logger.info("TRUNCATE completed in the sync table '{sync_table}'.".format(sync_table=self._rdl_tables_views['sync_table']))
                    self._rdl_sync_table_truncated = True

                result = self._db_client.copy(prefix=s3_path,
                                              table=self._rdl_tables_views['sync_table'],
                                              jsonas=json_as,
                                              compression='GZIP',
                                              maxerror=100000,
                                              truncatecolumns=True,
                                              acceptanydate=True,
                                              acceptinvchars=True,
                                              compupdate=False,
                                              statupdate=False)

                self._logger.info("COPY of the path '{s3_path}' completed' [Rows: {rows}]".format(s3_path=s3_path,
                                                                                                  rows=result['rowcount']))
                self._total_rows_affected += result['rowcount']
                self._ok_files.append(s3_path)
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._ko_files.append(s3_path)
            self._logger.error("Could not load the path '{s3_path}' into the table '{sync_table}', skipping loading. [{error}]".format(s3_path=s3_path,
                                                                                                                                       sync_table=self._rdl_tables_views['sync_table'],
                                                                                                                                       error=e))
            pass

        self._total_files_processed += 1

    def transform(self):
        """
        Transform data loaded in the sync table and insert it in the staging table (RDL)
        :return: None
        """
        try:
            if self._db_client:
                if self._total_rows_affected > 0:
                    # truncate staging table
                    self._db_client.truncate(self._rdl_tables_views['staging_table'])
                    self._logger.info("TRUNCATE completed in the staging table '{staging_table}'.".format(staging_table=self._rdl_tables_views['staging_table']))

                    # transform and insert data into staging table using transformation view
                    query = 'INSERT INTO {staging_table} SELECT * FROM {transformation_view};'.format(staging_table=self._rdl_tables_views['staging_table'],
                                                                                                      transformation_view=self._rdl_tables_views['transformation_view'])
                    result = self._db_client.execute(query)
                    self._logger.info("INSERT completed in the staging table '{staging_table}' [Rows: {rows}]".format(staging_table=self._rdl_tables_views['staging_table'],
                                                                                                                      rows=result['rowcount']))
                    if result['rowcount'] > 0:
                        self._rdl_staging_table_loaded = True
                        self._db_client.analyze(self._rdl_tables_views['staging_table'])

                else:
                    # checking why the the totals rows is equal to zero
                    if self._rdl_sync_table_truncated:
                        if len(self._ko_files) == self._total_files_processed:
                            extra_message = 'Check files, seems they are invalid or have any error.'
                        elif len(self._ok_files) == self._total_files_processed:
                            extra_message = 'Check files, seems they are empty.'
                        else:
                            extra_message = 'Check files, seems they are invalid/empty or have any error.'
                    else:
                        extra_message = 'Execute extract method to load it.'
                    raise Exception("Sync table '{sync_table}' is empty. {extra_message}".format(sync_table=self._rdl_tables_views['sync_table'],
                                                                                                 extra_message=extra_message))
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise

    def load(self):
        """
        Load data into the final table from the staging table [ODL]
        :return: None
        """
        try:
            if self._db_client:
                if self._rdl_staging_table_loaded:
                    # getting business region with data loaded
                    query = """SELECT DISTINCT 
                                    business_region     AS region,
                                    COUNT(*)            AS rowcount
                               FROM {staging_table} 
                               ORDER BY business_region;
                            """.format(staging_table=self._rdl_tables_views['staging_table'])

                    result = self._db_client.execute(query)
                    regions_with_data = result['data']

                    for row in regions_with_data:
                        if row.region == 'unknown':
                            self._logger.warning("Rows with 'unknown' business region will not moved to the hourly/tracking tables [Rows: {rows}]".format(rows=row.rowcount))
                        else:
                            # creating staging table
                            staging_table = self._odl_tables_views[row.region]['prefix'] + '_{epoch}_staging'.format(epoch=get_epoch_timestamp())
                            query = 'CREATE TEMP TABLE {staging_table} (LIKE: {template_table});'.format(staging_table=staging_table,
                                                                                                         template_table=self._odl_tables_views[row.region]['template_table'])

                            self._db_client.execute(query)
                            self._logger.debug("CREATE TEMP table '{staging_table}' completed.".format(staging_table=staging_table))

                            # inserting data into TEMP table
                            query = """
                                    INSERT INTO {staging_table}
                                    SELECT * FROM {transformation_view}
                                    WHERE business_region = '{region}';
                                    """.format(staging_table=staging_table,
                                               transformation_view=self._odl_tables_views[row.region]['transformation_view'],
                                               region=row.region)

                            result = self._db_client.execute(query)

                            if result['rowcount'] > 0:
                                self._logger.info("INSERT INTO TEMP table '{staging_table}' completed [Rows: {rows}]".format(staging_table=staging_table,
                                                                                                                             rows=result['rowcount']))
                                # selecting distinct months to load
                                query = """
                                        SELECT DISTINCT
                                            TO_CHAR(date_event_nk, 'YYYYMM') AS month_nk
                                        FROM {staging_table}
                                        WHERE date_event_nk IS NOT NULL;
                                        """.format(staging_table=staging_table)

                                result = self._db_client.execute(query)
                                months = result['data']

                                for month in months:
                                    # creating final table if does not exist
                                    tracking_table = self._odl_schema + '.' + self._odl_tables_views[row.region]['prefix'] + '_' + month
                                    query = 'CREATE TABLE IF NOT EXISTS {tracking_table} (LIKE: {template_table});'.format(tracking_table=tracking_table,
                                                                                                                           template_table=self._odl_tables_views[row.region]['template_table'])

                                    self._db_client.execute(query)
                                    self._logger.debug("CREATE table '{tracking_table}' completed.".format(tracking_table=tracking_table))

                                    # deleting data in tracking table
                                    query = """
                                        DELETE FROM {tracking_table}
                                        USING (SELECT DISTINCT 
                                                    server_path             AS server_path,
                                                    country_sk              AS country_sk,
                                                    min(time_event_local)   AS min_time_event_local,
                                                    max(time_event_local)   AS max_time_event_local
                                        FROM  {staging_table}) AS tmp
                                        WHERE {tracking_table}.server_path = tmp.server_path
                                        AND   {tracking_table}.country_sk = tmp.country_sk
                                        AND   {tracking_table}.time_event_local BETWEEN tmp.min_time_event_local AND tmp.max_time_event_local;
                                        """.format(tracking_table=tracking_table,
                                                   staging_table=staging_table)

                                    result = self._db_client.execute(query)
                                    self._logger.info("DELETE of data from tracking table '{tracking_table}' completed [Rows: {rows}]".format(tracking_table=tracking_table,
                                                                                                                                              rows=result['rowcount']))
                                    # inserting data in tracking table
                                    query = 'INSERT INTO {tracking_table} SELECT * FROM {staging_table};'.format(tracking_table=tracking_table,
                                                                                                                 staging_table=staging_table)

                                    result = self._db_client.execute(query)
                                    self._logger.info("INSERT INTO table '{tracking_table}' completed [Rows: {rows}]".format(tracking_table=tracking_table,
                                                                                                                             rows=result['rows']))

                                    # drop staging table
                                    self._db_client.drop(staging_table)
                            else:
                                self._logger.warning("No data loaded in TEMP table '{staging_table}'".format(staging_table=staging_table))

                            self._db_client.drop(staging_table)

                else:
                    if self._rdl_staging_table_truncated:
                        raise Exception("Staging table '{staging_table}' is empty.".format(staging_table=self._rdl_tables_views['staging_table']))
                    else:
                        raise Exception("Staging table '{staging_table}' was not loaded.".format(staging_table=self._rdl_tables_views['staging_table']))
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise


class ClassicStream(Hydra):
    def __init__(self, brand, region, channel, rdl_schema, odl_schema):
        """
        Constructor
        :param brand: brand name OLX or Letgo [String]
        :param region: classic region or business region name: CEE, SSA, MENA, MENAPK, ID, PH, SA, CEE,
                                                               LATAM. MEA, ASIA or EU
        :param channel: channel name: Android, iOS or Web [String]
        :param rdl_schema: raw data layer schema [String]
        :param odl_schema: operation data layer schema [String]
        """
        # super initialization
        Hydra.__init__(self, brand, channel, rdl_schema, odl_schema)

        # logger
        self._logger = logging.getLogger(__name__)

        # region
        self._region = region

        # RDL tables/views
        rdl_table_prefix = 'panamera{brand}_{region}_ninja_{channel}'.format(brand=self._brand,
                                                                             region=self._region,
                                                                             channel=channel)

        self._rdl_tables_views = {'prefix': rdl_table_prefix,
                                  'sync_table': '{rdl_schema}.{rdl_table_prefix}_sync'.format(rdl_schema=self._rdl_schema,
                                                                                              rdl_table_prefix=rdl_table_prefix),
                                  'staging_table': '{rdl_schema}.{rdl_table_prefix}_staging'.format(rdl_schema=self._rdl_schema,
                                                                                                    rdl_table_prefix=rdl_table_prefix),
                                  'transformation_view': '{rdl_schema}.{rdl_table_prefix}_transformation_view'.format(rdl_schema=self._rdl_schema,
                                                                                                                      rdl_table_prefix=rdl_table_prefix)
                                  }

        self._logger.debug(self._rdl_tables_views)

    def extract(self, s3_path, json_as):
        """
        Extract data from the S3 and copy it to the sync table
        :param s3_path: s3 path to json file to load [String]
        :param json_as: s3 path to json manifest or 'auto' option [String]
        :return: None
        """
        try:
            if self._db_client:
                if not self._rdl_sync_table_truncated:
                    self._db_client.truncate(self._rdl_tables_views['sync_table'])
                    self._logger.info("TRUNCATE completed in the sync table '{sync_table}'.".format(sync_table=self._rdl_tables_views['sync_table']))
                    self._rdl_sync_table_truncated = True

                result = self._db_client.copy(prefix=s3_path,
                                              table=self._rdl_tables_views['sync_table'],
                                              jsonas=json_as,
                                              compression='GZIP',
                                              maxerror=100000,
                                              truncatecolumns=True,
                                              acceptanydate=True,
                                              acceptinvchars=True,
                                              compupdate=False,
                                              statupdate=False)

                self._logger.info("COPY of the path '{s3_path}' completed' [Rows: {rows}]".format(s3_path=s3_path,
                                                                                                  rows=result['rowcount']))
                self._total_rows_affected += result['rowcount']
                self._ok_files.append(s3_path)
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._ko_files.append(s3_path)
            self._logger.error("Could not load the path '{s3_path}' into the table '{sync_table}', skipping loading. [{error}]".format(s3_path=s3_path,
                                                                                                                                       sync_table=self._rdl_tables_views['sync_table'],
                                                                                                                                       error=e))
            pass

        self._total_files_processed += 1

    def transform(self):
        """
        Transform data loaded in the sync table and insert it in the staging table (RDL)
        :return: None
        """
        try:
            if self._db_client:
                if self._total_rows_affected > 0:
                    # truncate staging table
                    self._db_client.truncate(self._rdl_tables_views['staging_table'])
                    self._logger.info("TRUNCATE completed in the staging table '{staging_table}'.".format(staging_table=self._rdl_tables_views['staging_table']))

                    # transform and insert data into staging table using transformation view
                    query = 'INSERT INTO {staging_table} SELECT * FROM {transformation_view};'.format(staging_table=self._rdl_tables_views['staging_table'],
                                                                                                      transformation_view=self._rdl_tables_views['transformation_view'])
                    result = self._db_client.execute(query)
                    self._logger.info("INSERT completed in the staging table '{staging_table}' [Rows: {rows}]".format(staging_table=self._rdl_tables_views['staging_table'],
                                                                                                                      rows=result['rowcount']))
                    if result['rowcount'] > 0:
                        self._rdl_staging_table_loaded = True
                        self._db_client.analyze(self._rdl_tables_views['staging_table'])

                else:
                    # checking why the the totals rows is equal to zero
                    if self._rdl_sync_table_truncated:
                        if len(self._ko_files) == self._total_files_processed:
                            extra_message = 'Check files, seems they are invalid or have any error.'
                        elif len(self._ok_files) == self._total_files_processed:
                            extra_message = 'Check files, seems they are empty.'
                        else:
                            extra_message = 'Check files, seems they are invalid/empty or have any error.'
                    else:
                        extra_message = 'Execute extract method to load it.'
                    raise Exception("Sync table '{sync_table}' is empty. {extra_message}".format(sync_table=self._rdl_tables_views['sync_table'],
                                                                                                 extra_message=extra_message))
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise

    def load(self):
        """
        Load data into the final table from the staging table [ODL]
        :return: None
        """
        try:
            if self._db_client:
                if self._rdl_staging_table_loaded:
                    # getting business region with data loaded
                    query = """SELECT DISTINCT 
                                    business_region     AS region,
                                    COUNT(*)            AS rowcount
                               FROM {staging_table} 
                               ORDER BY business_region;
                            """.format(staging_table=self._rdl_tables_views['staging_table'])

                    result = self._db_client.execute(query)
                    regions_with_data = result['data']

                    for row in regions_with_data:
                        if row.region == 'unknown':
                            self._logger.warning("Rows with 'unknown' business region will not moved to the hourly/tracking tables [Rows: {rows}]".format(rows=row.rowcount))
                        else:
                            # creating staging table
                            staging_table = self._odl_tables_views[row.region]['prefix'] + '_{epoch}_staging'.format(epoch=get_epoch_timestamp())
                            query = 'CREATE TEMP TABLE {staging_table} (LIKE: {template_table});'.format(staging_table=staging_table,
                                                                                                         template_table=self._odl_tables_views[row.region]['template_table'])

                            self._db_client.execute(query)
                            self._logger.debug("CREATE TEMP table '{staging_table}' completed.".format(staging_table=staging_table))

                            # inserting data into TEMP table
                            query = """
                                    INSERT INTO {staging_table}
                                    SELECT * FROM {transformation_view}
                                    WHERE business_region = '{region}';
                                    """.format(staging_table=staging_table,
                                               transformation_view=self._odl_tables_views[row.region]['transformation_view'],
                                               region=row.region)

                            result = self._db_client.execute(query)

                            if result['rowcount'] > 0:
                                self._logger.info("INSERT INTO TEMP table '{staging_table}' completed [Rows: {rows}]".format(staging_table=staging_table,
                                                                                                                             rows=result['rowcount']))
                                # selecting distinct months to load
                                query = """
                                        SELECT DISTINCT
                                            TO_CHAR(date_event_nk, 'YYYYMM') AS month_nk
                                        FROM {staging_table}
                                        WHERE date_event_nk IS NOT NULL;
                                        """.format(staging_table=staging_table)

                                result = self._db_client.execute(query)
                                months = result['data']

                                for month in months:
                                    # creating final table if does not exist
                                    tracking_table = self._odl_schema + '.' + self._odl_tables_views[row.region]['prefix'] + '_' + month
                                    query = 'CREATE TABLE IF NOT EXISTS {tracking_table} (LIKE: {template_table});'.format(tracking_table=tracking_table,
                                                                                                                           template_table=self._odl_tables_views[row.region]['template_table'])

                                    self._db_client.execute(query)
                                    self._logger.debug("CREATE table '{tracking_table}' completed.".format(tracking_table=tracking_table))

                                    # deleting data in tracking table
                                    query = """
                                        DELETE FROM {tracking_table}
                                        USING (SELECT DISTINCT 
                                                    server_path             AS server_path,
                                                    country_sk              AS country_sk,
                                                    min(time_event_local)   AS min_time_event_local,
                                                    max(time_event_local)   AS max_time_event_local
                                        FROM  {staging_table}) AS tmp
                                        WHERE {tracking_table}.server_path = tmp.server_path
                                        AND   {tracking_table}.country_sk = tmp.country_sk
                                        AND   {tracking_table}.time_event_local BETWEEN tmp.min_time_event_local AND tmp.max_time_event_local;
                                        """.format(tracking_table=tracking_table,
                                                   staging_table=staging_table)

                                    result = self._db_client.execute(query)
                                    self._logger.info("DELETE of data from tracking table '{tracking_table}' completed [Rows: {rows}]".format(tracking_table=tracking_table,
                                                                                                                                              rows=result['rowcount']))
                                    # inserting data in tracking table
                                    query = 'INSERT INTO {tracking_table} SELECT * FROM {staging_table};'.format(tracking_table=tracking_table,
                                                                                                                 staging_table=staging_table)

                                    result = self._db_client.execute(query)
                                    self._logger.info("INSERT INTO table '{tracking_table}' completed [Rows: {rows}]".format(tracking_table=tracking_table,
                                                                                                                             rows=result['rows']))

                                    # drop staging table
                                    self._db_client.drop(staging_table)
                            else:
                                self._logger.warning("No data loaded in TEMP table '{staging_table}'".format(staging_table=staging_table))

                            self._db_client.drop(staging_table)

                else:
                    if self._rdl_staging_table_truncated:
                        raise Exception("Staging table '{staging_table}' is empty.".format(staging_table=self._rdl_tables_views['staging_table']))
                    else:
                        raise Exception("Staging table '{staging_table}' was not loaded.".format(staging_table=self._rdl_tables_views['staging_table']))
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise

