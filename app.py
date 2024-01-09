import mysql.connector

# Master Database Configuration
master_config = {
    'host': 'ip_master',
    'user': 'name-user',
    'password': 'pass',
    'database': 'test',
}

# Slave Database Configuration
slave_config = {
    'host': 'localhost',
    'user': 'name_user',
    'password': 'pass',
    'database': 'test',
}

# Connect to the master database
master_conn = mysql.connector.connect(**master_config)
master_cursor = master_conn.cursor()

# Connect to the slave database
slave_conn = mysql.connector.connect(**slave_config)
slave_cursor = slave_conn.cursor()

# Create a table if it doesn't exist on both master and slave
table_creation_query = """
CREATE TABLE IF NOT EXISTS example_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data VARCHAR(255)
);
"""

master_cursor.execute(table_creation_query)
slave_cursor.execute(table_creation_query)

# Insert data into the master database
insert_query = "INSERT INTO example_table (data) VALUES (%s);"
data_to_insert = ("Master Data 1",)

master_cursor.execute(insert_query, data_to_insert)
master_conn.commit()

# Verify data on the slave
slave_cursor.execute("SELECT * FROM example_table;")
result = slave_cursor.fetchall()

print("Data on the slave:")
for row in result:
    print(row)

# Clean up
master_cursor.close()
master_conn.close()
slave_cursor.close()
slave_conn.close()
