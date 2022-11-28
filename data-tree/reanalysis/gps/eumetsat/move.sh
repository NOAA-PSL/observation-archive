aws s3 cp --profile=rnr-bdp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/gpsro/EUMETSAT/ s3://noaa-reanalyses-pds/observations/reanalysis/gps/eumetsat/ --recursive

aws s3 ls --profile=rnr-bdp --recursive --human-readable --summarize s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/gpsro/EUMETSAT/ 
#Total Objects: 22231 Total Size: 115.7 GiB
aws s3 ls --profile=rnr-bdp --recursive --human-readable --summarize  s3://noaa-reanalyses-pds/observations/reanalysis/gps/eumetsat/
#Total Objects: 22231 Total Size: 115.7 GiB

#aws s3 rm --profile=rnr-bdp --recursive s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/gpsro/EUMETSAT/
