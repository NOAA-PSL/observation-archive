aws s3 sync --profile=rnr-bdp log/ s3://noaa-reanalyses-pds/observations/reanalysis/ssu/1bssu/log/
aws s3 cp --profile=rnr-bdp CHANGELOG.md s3://noaa-reanalyses-pds/observations/reanalysis/ssu/1bssu/
aws s3 cp --profile=rnr-bdp README.md s3://noaa-reanalyses-pds/observations/reanalysis/ssu/1bssu/

 

