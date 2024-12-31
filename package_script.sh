#!/bin/bash

# Create a temporary directory for the files
mkdir -p temp_package

# Copy necessary files
cp app.py temp_package/
cp -r templates temp_package/
cp requirements.txt temp_package/
cp Dockerfile temp_package/
cp docker-compose.yml temp_package/
cp .dockerignore temp_package/
cp README.md temp_package/

# Create the archive
tar -czf qa_tools_app.tar.gz -C temp_package .

# Clean up
rm -rf temp_package

echo "Package created successfully: qa_tools_app.tar.gz"
echo "The package contains:"
echo "- app.py (main application)"
echo "- templates/ (HTML templates)"
echo "- requirements.txt (Python dependencies)"
echo "- Dockerfile"
echo "- docker-compose.yml"
echo "- .dockerignore"
echo "- README.md" 