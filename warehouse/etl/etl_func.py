# simple etl process use pandas
import logging
from datetime import datetime, timedelta

def yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    return f"{yesterday.strftime('%Y-%m-%d')} 00:00:00"

def upsert(source_table, target_table, sql, key, insert=False):
    from sqlalchemy import update
    import db.warehouse_db
    import db.source_db
    
    logging.basicConfig(level=logging.INFO)

    sSession = db.source_db.get_session()
    wSession = db.warehouse_db.get_session()

    try:
        with sSession() as source_session, wSession() as warehouse_session:
            logging.info(f"Starting ETL process for {target_table.__tablename__}")

            data = source_session.execute(sql).fetchall()

            if data:
                if insert:
                    logging.info(f"{len(data)} new records found in {source_table}")
                else:
                    logging.info(f"{len(data)} updated records found in {source_table}")

                params_dict = [dict(zip(key, record)) for record in data]

                if insert:
                    warehouse_session.execute(
                        statement=insert(target_table),
                        params=params_dict
                    )
                else:
                    warehouse_session.execute(
                        statement=update(target_table),
                        params=params_dict
                    )

                warehouse_session.commit()
                if insert:
                    logging.info(f"Inserted {len([params_dict])} records in {target_table.__tablename__}")
                else:
                    logging.info(f"Updated {len([params_dict])} records in {target_table.__tablename__}")
            else:
                logging.info(f"No new records found in {source_table}")

    except Exception as e:
        logging.error(f"Error in ETL process: {e}", exc_info=True)