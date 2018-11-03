import os as os
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np


#Dataset 1
df_1_compensation = pd.read_csv("data/compensation-of-employees-by-industry-at-current-prices-annual.csv")

# df_1_compensation.year = pd.to_datetime(df_1_compensation.year, format='%Y',errors="coerce")

#Dataset 2
df_2_rate_salary1 = pd.read_csv("data/graduate-employment-survey-ntu-nus-sit-smu-sutd.csv", encoding='latin-1')
df_2_rate_salary = df_2_rate_salary1.replace('na', np.nan).dropna()

df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('business', case=False), 'school'] = 'Business'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('engineering', case=False), 'school'] = 'Engineering'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('of science', case=False), 'school'] = 'Sciences'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('social', case=False), 'school'] = 'Humanities & Social Sciences'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('law', case=False), 'school'] = 'Law'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('design', case=False), 'school'] = 'Design'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('of art', case=False), 'school'] = 'Design'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('computing', case=False), 'school'] = 'Computing & Information Technology'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('tech', case=False), 'school'] = 'Computing & Information Technology'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('information', case=False), 'school'] = 'Computing & Information Technology'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('dentistry', case=False), 'school'] = 'Medicine'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('medicine', case=False), 'school'] = 'Medicine'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('accountancy', case=False), 'school'] = 'Business'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('economics', case=False), 'school'] = 'Business'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('music', case=False), 'school'] = 'Others'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('multidisciplinary', case=False), 'school'] = 'Others'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('education', case=False), 'school'] = 'Education'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('university', case=False), 'school'] = 'Others'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('college', case=False), 'school'] = 'Others'
df_2_rate_salary.loc[df_2_rate_salary['school'].str.contains('the', case=False), 'school'] = 'Others'

#Dataset 3
df_3_jobs1 = pd.read_csv("data/job-vacancy-by-industry-level1.csv")
df_3_jobs2 = pd.read_csv("data/job-vacancy-by-industry-level2.csv")
df_3_jobs3 = pd.read_csv("data/job-vacancy-by-industry-level3.csv")

df_all_jobs = pd.concat([df_3_jobs1,df_3_jobs2,df_3_jobs3], axis=0, sort=True)
for i in np.arange(1990,2019):
    df_all_jobs.loc[df_all_jobs['quarter'].str.contains(str(i)), 'quarter'] = str(i)

df_all_jobs2 = df_3_jobs3
df_all_jobs2.drop(['industry2','industry3'], axis=1, inplace=True)
df_all_jobs2 = df_all_jobs2[df_all_jobs2.job_vacancy.str.contains("-") == False]
df_all_jobs2.job_vacancy = df_all_jobs2.job_vacancy.astype(float).fillna(0.0)
df_all_jobs2.drop_duplicates(['quarter', 'industry1', 'job_vacancy']).groupby('quarter')['job_vacancy'].mean()



#Dataset 4
df_4_IT = pd.read_csv("data/Data USA - Bar Chart of Yearly Income for Common Jobs for Information Technology Majors-1.csv")
df_5_IT = pd.read_csv("data/Data USA - Bar Chart of Yearly Income for Common Jobs for Information Technology Majors-2.csv")
df_6_IT = pd.read_csv("data/Data USA - Bar Chart of Yearly Income for Common Jobs for Information Technology Majors-3.csv")
#Merge Datasets
df_all_IT = pd.concat([df_4_IT,df_5_IT,df_6_IT], axis=0)



#Store data in MongoDB
# MONGO_URL = os.environ.get('MONGOHQ_URL') 
# client = MongoClient(MONGO_URL)
# if 'app105426028' in client.list_database_names():
#     client.drop_database('app105426028')

client = MongoClient('mongodb://erra:qwerty123@ds121312.mlab.com:21312/pdsca2victoria')



db = client.pdsca2victoria
collection1 = db.Compensation
collection2 = db.RateSalary
collection3 = db.Jobs
collection32 = db.Jobs2
collection4 = db.IT


# if 'app105426028' not in client.list_database_names():

collection1.insert_many(df_1_compensation.to_dict("records"))
collection2.insert_many(df_2_rate_salary.to_dict("records"))
collection3.insert_many(df_all_jobs.to_dict("records"))
collection32.insert_many(df_all_jobs2.to_dict("records"))
collection4.insert_many(df_all_IT.to_dict("records"))

