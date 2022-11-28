aws s3 sync --profile=rnr-bdp log/ s3://noaa-reanalyses-pds/observations/reanalysis/conv/prepbufr.acft_profiles/log/
aws s3 cp --profile=rnr-bdp CHANGELOG.md s3://noaa-reanalyses-pds/observations/reanalysis/conv/prepbufr.acft_profiles/
aws s3 cp --profile=rnr-bdp README.md s3://noaa-reanalyses-pds/observations/reanalysis/conv/prepbufr.acft_profiles/

 

