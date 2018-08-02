#!/usr/bin/env python

from .hydra import Hydra
from datetime import datetime
from .extras import get_epoch_timestamp


class ClassicStream(Hydra):
    def __init__(self, brand, region, channel, rdl_schema, odl_schema, streaming, level='INFO'):
        """
        Constructor
        :param brand: brand name OLX or Letgo [String]
        :param region: classic region or business region name: CEE, SSA, MENA, MENAPK, ID, PH, SA, CEE,
                                                               LATAM. MEA, ASIA or EU
        :param channel: channel name: Android, iOS or Web [String]
        :param rdl_schema: raw data layer schema [String]
        :param odl_schema: operation data layer schema [String]
        :param streaming: true is loading is coming from kinesis, false from file [Boolean]
        :param level: logging level [String]
        """
        # super initialization
        Hydra.__init__(self, brand, channel, rdl_schema, odl_schema, streaming, level)

        # prefix
        self._table_prefix = 'classic{brand}_{region}'.format(brand=self._brand,
                                                              region=region)

    def load(self):
        """
        Load data into the final table from the staging table [ODL]
        :return: None
        """
        try:
            if self._db_client:
                # starting timer
                start = datetime.now()

                # counters
                total_rows = 0
                inserted_rows = 0
                unknown_rows = 0

                # getting business region with data loaded
                staging_table = self._get_rdl_tables_and_views()['StagingTable']
                query = """SELECT DISTINCT 
                                business_region     AS region,
                                COUNT(*)            AS rowcount
                           FROM {staging_table} 
                           GROUP BY business_region
                           ORDER BY business_region
                           ;
                        """.format(staging_table=staging_table)

                result = self._db_client.execute(query)
                regions_with_data = result['data']

                for row in regions_with_data:
                    total_rows += row.rowcount

                    if row.region == 'unknown':
                        unknown_rows += row.rowcount
                    else:
                        self._logger.info('>>> ' + row.region.upper())

                        # creating staging table
                        template_table = self._get_odl_tables_and_views()[row.region]['TemplateTable']
                        staging_table = template_table.replace('{odl_schema}.'.format(odl_schema=self._odl_schema), '').replace('_template', '_{business_region}_{epoch}_staging'.format(business_region=row.region,
                                                                                                                                                                                         epoch=get_epoch_timestamp())).strip()

                        query = 'CREATE TEMP TABLE {staging_table} (LIKE {template_table});'.format(staging_table=staging_table,
                                                                                                    template_table=template_table)

                        self._db_client.execute(query)
                        self._logger.info("CREATE TEMP table '{staging_table}' completed".format(staging_table=staging_table))

                        # inserting data into TEMP table
                        transformation_view = self._get_odl_tables_and_views()[row.region]['TransformationView']
                        query = """
                                INSERT INTO {staging_table}
                                SELECT * FROM {transformation_view}
                                WHERE region_nk = '{region}';
                                """.format(staging_table=staging_table,
                                           transformation_view=transformation_view,
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
                                tracking_table = template_table.replace('_template', '_{month}'.format(month=month.month_nk))
                                query = 'CREATE TABLE IF NOT EXISTS {tracking_table} (LIKE {template_table});'.format(tracking_table=tracking_table,
                                                                                                                      template_table=template_table)

                                self._db_client.execute(query)

                                # deleting data in tracking table
                                if not self._streaming:
                                    query = """
                                        DELETE FROM {tracking_table}
                                        USING (SELECT DISTINCT 
                                                    server_path             AS server_path,
                                                    country_sk              AS country_sk,
                                                    min(time_event_local)   AS min_time_event_local,
                                                    max(time_event_local)   AS max_time_event_local
                                               FROM  {staging_table}
                                               GROUP BY 1, 2
                                               ORDER BY 1, 2) AS tmp
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
                                                                                                                         rows=result['rowcount']))

                                inserted_rows += result['rowcount']

                            # drop staging table
                            self._db_client.drop(staging_table)

                            # update log table
                            if self._streaming:
                                self._update_sequence('loaded')
                                self._logger.info("Updated log table '{log_table} SET loaded = TRUE'".format(log_table=self._get_log_table()))
                        else:
                            self._logger.warning("No data loaded in TEMP table '{staging_table}'".format(staging_table=staging_table))
                    self._logger.info('\r')

                # ending timer
                end = datetime.now()
                elapsed_time = (end-start).total_seconds()

                self._logger.info('+++++++++++++++++++++++++++++++++++++')
                self._logger.info('|             STATISTICS            |')
                self._logger.info('+++++++++++++++++++++++++++++++++++++')
                self._logger.info('| Unknown region: {:12d} rows |'.format(unknown_rows))
                self._logger.info('| Bots/Blacklist: {:12d} rows |'.format(total_rows - unknown_rows - inserted_rows))
                self._logger.info('| Inserted:       {:12d} rows |'.format(inserted_rows))
                self._logger.info('| Elapsed time:   {:12d} sec  |'.format(int(elapsed_time)))
                self._logger.info('+++++++++++++++++++++++++++++++++++++')
            else:
                raise Exception('No database connection established. Connect to database before to run any method.')
        except Exception as e:
            self._logger.error(repr(e))
            raise

