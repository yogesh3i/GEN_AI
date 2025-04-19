# make connection to the database 
import pymysql
db = pymysql.connect(host='localhost',user='root',password='Yogesh@123',database='student')

# impliment the cursor which will help to interact and execute the sql querys on the database 
cursor = db.cursor()

# create table in the database 

query = 'CREATE TABLE stu_info(NAME VARCHAR(20), CLASS VARCHAR(25), SECTION VARCHAR(10), MARKS INT)'

cursor.execute(query)

# insert records into the data 

query = """
INSERT INTO stu_info (NAME, CLASS, SECTION, MARKS) VALUES
('Rahul', '10th', 'A', 88),
('Priya', '10th', 'B', 92),
('Aman', '9th', 'A', 75),
('Sneha', '9th', 'C', 81),
('Vikram', '8th', 'B', 69)
"""

cursor.execute(query)
db.commit()

# display the data 

query = 'SELECT * FROM stu_info;'
cursor.execute(query)
data = cursor.fetchall()

for row in data:
    print(row)


# commit the changes and close the db connection 
db.commit()
db.close()