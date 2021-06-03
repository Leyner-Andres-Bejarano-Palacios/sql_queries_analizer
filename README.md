# sql_queries_analizer

python code created to find bad practices (a list of bad practices defined by the organization where I was working at that moment) in the sql quries.


## The context
There was a limited amount of servers for every big data job in the company, so in order to give all of the users the best possible experience every sql script to be executed in the
clusters must compliance with a group of rules established by the company.

## The rules

1. every query must specify the partition where the desired data is stored

2. every query must specify the desired columns

3. every query must use 7 joins at most

4. every query must have maximun 50 cases

5. every case clause mush have at must 20 when clauses

## The problem

There was a lot of really large sql scripts to be analized, this resulted in developers not been able to do other more interesting task that not only bring a great return of investment to the company but also great pride to the developers.


## The solution

Using regular expresions to detect the piece of code where any of these rules was been broken

#### The regex to detect the rule # 1

This is the most complex rule and it happen in several phases.

##### phase1, phase2 and phase3

In phase #1 (method __fn_find_referenced_tables) we generate a list of every table in the cluster (the rule does not apply on tables created by the user). we check if the name of those tables is present in the query. This is a simple literal match looking for specific names in the string

Phase #2 check for reference to partitions. References to partitions are sql sentences of the form "from ingestion_year"

Phase #3 create a dictionary of every alias used in the sql query



