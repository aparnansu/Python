import os
import re

# Function to group statements by table name
def group_statements(statements):
    groups = {}
    current_group = []

    for statement in statements:
        match = re.match(r'(DROP TABLE|CREATE TABLE) (\w+)', statement)
        if match:
            table_name = match.group(2)
            if table_name not in groups:
                groups[table_name] = []
            if current_group:
                groups[current_group[0]].extend(current_group[1:])
                current_group = []
            groups[table_name].append(statement)
        else:
            current_group.append(statement)

    if current_group:
        groups[current_group[0]].extend(current_group[1:])

    return groups

# Function to write grouped statements to files
def write_to_files(groups):
    for table_name, statements in groups.items():
        with open(f"{table_name}_DDL.sql", "w") as f:
            f.write('\n'.join(statements))

# Directory containing input files
input_directory = "input_files"

# Loop through each file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_directory, filename)
        
        # Read statements from input file
        with open(file_path, "r") as file:
            statements = file.read().split(';')

        # Group statements by table name
        groups = group_statements(statements)

        # Write grouped statements to files
        write_to_files(groups)

print("Files created successfully.")
