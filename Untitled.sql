EXECUTE NOTEBOOK PROJECT DEMO_DB.PROD_SCHEMA.DEMO_PIPELINES_NP
                MAIN_FILE = '02_load_daily_city_metrics.ipynb'
                COMPUTE_POOL = SYSTEM_COMPUTE_POOL_CPU
                RUNTIME = 'V2.5-CPU-PY3.12'
                QUERY_WAREHOUSE = DEMO_WH
                ARGUMENTS = '--database-name DEMO_DB --schema-name PROD_SCHEMA'