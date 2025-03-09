# globant_challenge
## Introduction
I completed Section 2. In this document, I will explain what I did, why I did it that way, and provide all the steps you need to follow to achieve the same results, including which files to use.

First, due to time constraints, I was only able to finish Section 2. However, I will explain the entire solution as I would have if I had more time for development and testing. I will also discuss the obstacles I encountered while working on the challenge.

## Development Section 2

### Insert Data 
Since I couldn't insert the data in Section 1, I did this. First, I created a bucket named files-challenge where I uploaded the three files:
```
	* departments.csv
	* hired_employees.csv
	* jobs.csv
```

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

 
	<img width="954" alt="instancia" src="https://github.com/user-attachments/assets/82787f91-41c7-4c6f-b80a-2cbcdbc54f83" />


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
		gcloud sql import csv my-database gs://files-challenge/departments.csv \
		  --database=postgres --table=departments --columns="id,department"
    	
	*For hired_employees:
		gcloud sql import csv my-database gs://files-challenge/hired_employees.csv \
		  --database=postgres --table=hired_employees --columns="id,name,datetime,department_id,job_id"
    	*For jobs:
		gcloud sql import csv my-database gs://files-challenge/jobs.csv \
		  --database=postgres --table=jobs --columns="id,job"
    For each table, it is now populated, and here is the evidence:

For each table, it is now populated, and here is the evidence:
* Departments:
<img width="907" alt="departments" src="https://github.com/user-attachments/assets/e81cddcc-2903-43e5-b993-1ff7d762b39a" />

* Hired_Employees:
<img width="923" alt="hired_employees" src="https://github.com/user-attachments/assets/8552721e-6978-49c0-8c45-d2041f632eb3" />

* Jobs:
<img width="916" alt="jobs" src="https://github.com/user-attachments/assets/06907411-7ce2-4421-8150-8d1cfadeab2c" />

### Requirements

The stakeholders ask for some specific metrics they need. So I have to create an end-point for each requirement and I did it with this steps:

#### Step 1:
I logged in with my credentials so that I wouldn’t have to enter them again later. However, a good practice is to access using a .json file containing the credentials but I didn't because of time. I used this command:
```
gcloud auth login
```

#### Step 2: 
I configure it to set my GCP project with this command:
```
gcloud config set project challenge-de
```

#### Step 3:
I enabled the permissions to work with these services using this command:

```
gcloud services enable sqladmin.googleapis.com
```

#### Step 4:
I had to install this connector to connect to Cloud SQL. I used this repository: https://github.com/GoogleCloudPlatform/cloud-sql-python-connector, with this command:
```
pip install "cloud-sql-python-connector[pg8000]"
```

#### Step 5:
I set the environment variables.
```
set INSTANCE_CONNECTION_NAME=challenge-de:southamerica-west1:my-database
set DB_USER=postgres
set DB_PASSWORD=dominga01
set DB_NAME=postgres
```

#### Step 6:
I tested the environment variables using the code in the file test_env.py.
```
python test_env.py
```

#### Step 7:
I tested the connection to the instance using the code in the conn_test.py file.
```
python conn_test.py
```


#### Step 8:
I executed the main app's code with this command:
```
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Step 9:
I visualized the endpoints by checking these URLs:

http://127.0.0.1:8000/employees-by-quarter

http://127.0.0.1:8000/departments-above-average


Here are the images of each requirement as evidence:

1) Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.

<img width="956" alt="number_employees_2021" src="https://github.com/user-attachments/assets/abea8bf0-d53f-473f-9a23-78c53f2faa5a" />


2) List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

 
  <img width="959" alt="list_employees_depto_2021" src="https://github.com/user-attachments/assets/74bccd69-c807-4819-82d3-39be11fd0948" />


