@echo off

echo Running extract scripts...
python -m extract.cicese_extract
python -m extract.copernicus_extract
python -m extract.globcolour_extract

echo Running transform scripts...
python -m transform.cicese_transform
python -m transform.copernicus_transform
python -m transform.globcolour_transform


echo Running load scripts...
python -m load.cicese_load
python -m load.copernicus_load
python -m load.globcolour_load

echo Done.