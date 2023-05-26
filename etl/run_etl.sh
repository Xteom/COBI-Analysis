#!/bin/bash

# Run all extract scripts
echo "Running extract scripts..."
python -m extract.cicese_extract
python -m extract.copernicus_extract
python -m extract.globcolour_extract

# Run all transform scripts
echo "Running transform scripts..."
python -m transform.cicese_transform
python -m transform.copernicus_transform
python -m transform.globcolour_transform

# Run all load scripts
echo "Running load scripts..."
python -m load.cicese_load
python -m load.copernicus_load
python -m load.globcolour_load

echo "Done."

# Load the data from data/copericus/processed into the s3 bucket
echo "Loading data into s3 bucket..."
aws s3 cp data/copericus/processed s3://cobi-clean-data-2023/copernicus/processed --recursive