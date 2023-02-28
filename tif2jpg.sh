#!/bin/bash

for f in *.tif
do 
  echo "converting $f"
  convert $f -channel RGB -threshold 95% jpg/${f%%.tif}.jpg
done

mv page*.tif ./conversion_sources/
