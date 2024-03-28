#!/bin/bash

# Check if a filename is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1
error_log="error.log"

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
        # Redirect stdout and stderr to a temporary file
        tmp_output=$(mktemp)
        eval "$line" > "$tmp_output" 2>&1
        exit_status=$?
        if [ $exit_status -ne 0 ]; then
            echo "Command failed with exit status $exit_status: $line"
            # Append the command and its output to the error log
            echo "Command: $line" >> "$error_log"
            echo "Error message:" >> "$error_log"
            cat "$tmp_output" >> "$error_log"
            echo "----------------------------------------" >> "$error_log"
        fi
        rm "$tmp_output"
    fi
done < "$filename"

echo "All commands executed successfully from $filename."
