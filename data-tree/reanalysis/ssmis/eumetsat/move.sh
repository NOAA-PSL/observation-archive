aws s3 cp --profile=rnr-bdp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/SSMIS/EUMETSAT/ s3://noaa-reanalyses-pds/observations/reanalysis/ssmis/eumetsat/ --recursive #--dryrun

aws s3 ls --profile=rnr-bdp --recursive --human-readable --summarize s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/SSMIS/EUMETSAT/ 
#Total Objects: 14766, Total Size: 1.4 TiB

aws s3 ls --profile=rnr-bdp --recursive --human-readable --summarize  s3://noaa-reanalyses-pds/observations/reanalysis/ssmis/eumetsat/
#Total Objects: 14766, Total Size: 1.4 TiB

#aws s3 rm --profile=rnr-bdp --recursive s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/SSMIS/EUMETSAT/ --dryrun
