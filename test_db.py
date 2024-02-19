import sqlite3

database_path = 'user_data.db'

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

new_data = {'Name': 'John Doe', 'Email': 'johndoe@gmail.com'}

for table in tables:
    table_name = table[0]
    print(f'\nContents of {table_name} table:')

    # Fetch column names
    cursor.execute(f'PRAGMA table_info({table_name});')
    columns = [column[1] for column in cursor.fetchall()]
    print(f'Columns: {columns}')

    # Fetch table content
    cursor.execute(f'SELECT * FROM {table_name};')
    table_content = cursor.fetchall()
    print(f'Content: {table_content}')

    # Check if 'Name' exists in the column names
    if 'Name' in columns:
        # Check if 'John Doe' exists in the first row
        if table_content and table_content[0][columns.index('Name')] != 'John Doe':
            # Update the table with new_data
            cursor.execute(f'UPDATE {table_name} SET Name=?, Email=? WHERE ROWID=1;', (new_data['Name'], new_data['Email']))
            connection.commit()
            print("Table updated with new_data.")
        else:
            print("John Doe already exists in the first row of the table.")
    else:
        print("'Name' column does not exist in the table.")

    for row in table_content:
        print(row)

connection.close()
