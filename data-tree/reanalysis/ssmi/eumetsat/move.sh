aws s3 cp --profile=rnr-bdp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/SSMI/EUMETSAT/ s3://noaa-reanalyses-pds/observations/reanalysis/ssmi/eumetsat/ --recursive #--dryrun

aws s3 ls --profile=rnr-bdp --recursive --human-readable --summarize s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/SSMI/EUMETSAT/ 
#Total Objects: 21889, Total Size: 350.9 GiB

aws s3 ls --profile=rnr-bdp --recursive --human-readable --summarize  s3://noaa-reanalyses-pds/observations/reanalysis/ssmi/eumetsat/
#Total Objects: 21889, Total Size: 350.9 GiB

#aws s3 rm --profile=rnr-bdp --recursive s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/SSMI/EUMETSAT/ --dryrun

