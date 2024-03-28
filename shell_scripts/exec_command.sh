#!/bin/bash

# Check if a filename is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi

# Read the file line by line and execute each line as a command
while IFS= read -r line; do
    # Skip empty lines and lines starting with #
    if [ -n "$line" ] && [ "${line:0:1}" != "#" ]; then
        echo "Executing: $line"
        eval "$line"
        exit_status=$?
        if [ $exit_status -ne 0 ]; then
            echo "Command failed with exit status $exit_status: $line"
            echo "Capturing error..."
            echo "Error message: $line" >> error.log
        fi
    fi
done < "$filename"

echo "All commands executed successfully from $filename."
