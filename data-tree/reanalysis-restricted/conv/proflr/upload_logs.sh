aws s3 sync --profile=psl-tt log/ s3://na-stage.us-east-2.noaa-nasa-share/noaa/reanalysis-restricted/conv/proflr/log/
aws s3 cp --profile=psl-tt CHANGELOG.md s3://na-stage.us-east-2.noaa-nasa-share/noaa/reanalysis-restricted/conv/proflr/
aws s3 cp --profile=psl-tt README.md s3://na-stage.us-east-2.noaa-nasa-share/noaa/reanalysis-restricted/conv/proflr/

 
