#------------------------------------------------------------------------------
# Hands-On Lab: Intro to Data Engineering with Notebooks
# Script:       deploy_notebooks.py
# Author:       Jeremiah Hansen
# Last Updated: 2/12/2026
#------------------------------------------------------------------------------

from snowflake.snowpark import Session


def main(session, database_name, schema_name, notebook_project_name, local_folder_path):
    # stable named stage instead of the random session temp stage
    deploy_stage = f"@{database_name}.{schema_name}.NB_DEPLOY_STAGE"
    session.sql(f"CREATE STAGE IF NOT EXISTS {database_name}.{schema_name}.NB_DEPLOY_STAGE").collect()
    # session.sql(f"REMOVE {deploy_stage}").collect()

    print(f"Uploading files from: {local_folder_path}")
    session.file.put(f"file://{local_folder_path}/*", deploy_stage, auto_compress=False, overwrite=True)

    result = session.sql(f"SHOW NOTEBOOK PROJECTS IN {database_name}.{schema_name}").collect()
    project_exists = any(row["name"] == notebook_project_name for row in result)

    full = f"{database_name}.{schema_name}.{notebook_project_name}"
    if project_exists:
        session.sql(f"ALTER NOTEBOOK PROJECT {full} ADD VERSION FROM '{deploy_stage}'").collect()
    else:
        session.sql(f"CREATE NOTEBOOK PROJECT {full} FROM '{deploy_stage}'").collect()
    return f"{full} deployed"


# For local debugging
if __name__ == "__main__":
    import sys
    from session_utils import get_snowpark_session

    # Get a Snowpark session (works in notebook, local, and CI/CD)
    # Note: Session is intentionally never closed to avoid issues in notebooks
    session = get_snowpark_session()

    if len(sys.argv) > 4:
        print(main(session, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        print("Usage: python deploy_notebooks.py <database> <schema> <notebook_project> <local_folder_path>")
