# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:06:23 2020

@author: LiamGalvin
"""


import pandas as pd

df = pd.read_csv("glassdoor_jobs.csv")

# TODO
# salary parsing

# remove rows with -1 in salary
df = df[df['Salary Estimate'] != '-1']

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0] ) 
minus_kd = salary.apply(lambda x: x.replace('K', '').replace('$',''))

df['employer_provided'] =  df['Salary Estimate'].apply(lambda x: 1 if "employer provided salary:" in x.lower() else 0)
df['hourly'] =  df['Salary Estimate'].apply(lambda x: 1 if "por hora" in x.lower() else 0)

minus_text = minus_kd.apply(lambda x: x.replace('Por hora', ''))
df['min_salary'] = minus_text.apply(lambda x: int(x.split('-')[0].strip()) ) 
df['max_salary'] = minus_text.apply(lambda x: int(x.split('-')[1].strip()) ) 
df['avg_salry'] = (df.min_salary + df.max_salary)/2

# Company name text only
df['company_text'] = df.apply(lambda x : x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)



# state field

df['job_state'] = df['Location'].apply(lambda x: x.strip().split(', ')[1] if len(x.strip().split(', ')) > 1 else -1 )
# remove entries where job state = -1
df = df[df['job_state'] != -1]

df.job_state.value_counts()

df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

# age of company 

df['age'] = df.Founded.apply(lambda x: x if x < 0 else 2020 - x)

# parsing of job description (python etc.)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0 )
#R Studio
df['r_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0 )
#spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0 )
#aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0 )
#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0 )


# save csv

df.to_csv("salary_data_cleaned.csv", index = False)