# globant_challenge
## Introduction
I completed Section 2. In this document, I will explain what I did, why I did it that way, and provide all the steps you need to follow to achieve the same results, including which files to use.

First, due to time constraints, I was only able to finish Section 2. However, I will explain the entire solution as I would have if I had more time for development and testing. I will also discuss the obstacles I encountered while working on the challenge.

## Development Section 2

Since I couldn't insert the data in Section 1, I did this. First, I created a bucket named files-challenge where I uploaded the three files:
	+ departments.csv
	+ hired_employees.csv
	+ jobs.csv

Second, I created the instance in GCP with the following description:
	
	connectionName: challenge-de:southamerica-west1:my-database
	createTime: '2025-03-05T21:12:44.766Z'
	databaseVersion: POSTGRES_16
	failoverReplica:
	  available: true
	instanceType: CLOUD_SQL_INSTANCE
	ipAddresses:
	- ipAddress: 34.176.167.69
	  type: PRIMARY
	- ipAddress: 10.52.160.4
	  type: PRIVATE
	name: my-database
	project: challenge-de
	region: southamerica-west1
	

After the instance was created, I had to create three tables for each file, and I used the following queries:

	* For departments:

		CREATE TABLE departments (
		    id INTEGER PRIMARY KEY,
		    department VARCHAR(255)
		);


	* For hired_employees:

		CREATE TABLE hired_employees (
		    id INTEGER PRIMARY KEY,
		    name VARCHAR(255),
		    datetime TIMESTAMP,
		    department_id INTEGER,
		    job_id INTEGER
		);

	* For jobs:
		
		CREATE TABLE jobs (
	    id INTEGER PRIMARY KEY,
	    job VARCHAR(255)
		);

After that, I modified the IAM policy of the bucket in GCP, with this command:
```
gsutil iam ch serviceAccount:p125245851199-txxhzb@gcp-sa-cloud-sql.iam.gserviceaccount.com:objectViewer gs://files-challenge
```

I check if the bucket has the necessary permissions with this command:
```
gsutil iam get gs://files-challenge
```

Then, I populated the tables in Cloud SQL for each table with this command:


	* For departments:
		```
		gcloud sql import csv my-database gs://files-challenge/departments.csv \
		  --database=postgres --table=departments --columns="id,department"
		```
	*For hired_employees:
		```
		gcloud sql import csv my-database gs://files-challenge/hired_employees.csv \
		  --database=postgres --table=hired_employees --columns="id,name,datetime,department_id,job_id"
		```
	*For jobs:
		```
		gcloud sql import csv my-database gs://files-challenge/jobs.csv \
		  --database=postgres --table=jobs --columns="id,job"
		```


