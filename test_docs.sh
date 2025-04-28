#!/bin/bash

# Test if mkdocs can build the documentation
echo "Testing MkDocs build..."

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "Error: mkdocs is not installed. Please install it with 'pip install mkdocs'."
    exit 1
fi

# Try to build the documentation
echo "Building documentation..."
mkdocs build --strict

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Documentation built successfully! The static site is in the 'site' directory."
    echo "You can view it by running 'mkdocs serve' and visiting http://localhost:8000"
else
    echo "Error: Documentation build failed. Please check the error messages above."
    exit 1
fi