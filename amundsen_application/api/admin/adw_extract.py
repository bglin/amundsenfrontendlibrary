# import pandas as pd
# import numpy as np
# import os
# import subprocess
# import cx_Oracle


# def connect_db(user,passwd,dsn):
#     db = cx_Oracle.connect(user= user, password= passwd,dsn= dsn)
#     return db

# ## will accept inputs from react frontend

# def query_db(db):
#     ##queries
#     sample_col = "SELECT column_name,data_type,data_length,column_id,table_name FROM user_tab_columns ORDER BY TABLE_NAME,COLUMN_ID"
#     sample_table = "SELECT table_name,cluster_name FROM USER_ALL_TABLES"

#     ##query results
#     result_col = pd.read_sql(sample_col, con=db)
#     result_table = pd.read_sql(sample_table, con=db)

#     return result_col,result_table

# ## data wrangling sample_col
# def sample_col(result_col):

#     def coltype_fun(df):
#         return (df[1] +'(' + str(df[2]) + ')')

#     result_col['col_type'] = result_col.apply(coltype_fun,axis=1)

#     result_col.drop(['DATA_TYPE','DATA_LENGTH'],axis=1,inplace=True)

#     result_col['table_desc']= 'AMUNDSEN'
#     result_col['database']= 'ADB'
#     result_col['cluster']= 'gold'
#     result_col['schema_name']= 'test_schema'
#     result_col['description']= ''

#     result_col.rename(columns={'COLUMN_ID': 'sort_order','COLUMN_NAME':'name','TABLE_NAME':'table_name'},inplace=True)
#     result_col = result_col[['name', 'description','col_type','sort_order','database','cluster','schema_name','table_name','table_desc']]

#     return result_col


# def sample_table(result_table):
#     ## Alot of hardcoded values
#     default_cluster_name = 'gold'
#     default_db_name ='ADB'
#     default_table_desc = 'AMUNDSEN'
#     default_schema_name = 'test_schema'

#     ## data wrangling sample_table
#     result_table['database'] =default_db_name
#     result_table['cluster'] = default_cluster_name
#     result_table['table_desc'] = default_table_desc
#     result_table['schema_name']= default_schema_name

#     result_table.rename(columns={'CLUSTER_NAME': 'cluster_name','TABLE_NAME':'table_name'},inplace=True)
#     result_table = result_table[['database','cluster','schema_name','table_name','table_desc']]

#     return result_table

# def sample_col_usage(result_col):
#     ## Alot of hardcoded values
#     default_cluster_name = 'gold'
#     default_db_name ='ADB'
#     default_table_desc = 'AMUNDSEN'
#     default_schema_name = 'test_schema'

#     ##data wrangling sample_col_usage
#     result_usage=result_col.loc[:,['table_name','name']]
#     result_usage.rename(columns={'name':'column_name'},inplace=True)
#     result_usage['database']=default_db_name
#     result_usage['cluster']=default_cluster_name
#     result_usage['schema_name']=default_schema_name
#     result_usage['user_email']='test@oracle.com'
#     result_usage['read_count']=pd.Series(np.random.randint(0,1000+1) for n in range(len(result_usage.index)))
#     result_usage=result_usage[['database','cluster','schema_name','table_name','column_name','user_email','read_count']]

#     return result_usage

# ## sample_user table
# def sample_user():
#     result_user=pd.DataFrame(data=[['test@oracle.com','Bruno','Lin','Bruno Lin','bglin','Burlington Hub','Solution Engineer','manager.test@oracle.com','bglin']],
#     columns=['email','first_name','last_name','name','github_username','team_name','employee_type','manager_email','slack_id'])

#     return result_user

# ## sample app
# def sample_app(result_usage):

#     col_list=list(result_usage['column_name'])
#     sample_app=pd.DataFrame(['ADB.test_schema.{}'.format(item) for item in col_list])
#     sample_app['dag_id']='event_test'
#     sample_app['exec_date']='13-Sep-19'
#     sample_app['application_url_template']='https://airflow_host.net/admin/airflow/tree?dag_id={dag_id}'
#     sample_app.rename(columns={0:'task_id'},inplace=True)

#     return sample_app


# def write_to_csv(result_col,result_table,result_usage,result_user,sample_app,basepath):

#     example_path='example/sample_data'
#     # write to csv
#     result_col.to_csv(os.path.join(basepath,example_path,'sample_col.csv'), index=False)
#     result_table.to_csv(os.path.join(basepath,example_path,'sample_table.csv'), index=False)
#     result_usage.to_csv(os.path.join(basepath,example_path,'sample_column_usage.csv'), index=False)
#     result_user.to_csv(os.path.join(basepath,example_path,'sample_user.csv'), index=False)
#     sample_app.to_csv(os.path.join(basepath,example_path,'sample_application.csv'), index=False)


# python_bin='/Users/bglin/amundsendatabuilder/venv/bin/python'
# script_file = "/Users/bglin/amundsendatabuilder/example/scripts/sample_data_loader.py"

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

# with cd('/Users/bglin/amundsendatabuilder'):
#     subprocess.Popen([python_bin, script_file])
