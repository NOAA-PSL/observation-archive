# Jack W. has compiled some merged repro and original satwinds in his dorectory s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/
# this moves them to s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/

aws s3 --recursive --profile=rnr-bdp cp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/ s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/

#had a typo when i ran the command 1 above. here is a quick fix
aws s3 --recursive --profile=rnr-bdp cp observations/reanalysis/amv/merged/ s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/

#move read me data
aws s3 --recursive --profile=rnr-bdp cp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/README s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/

#remove original data from reprocessed-from-jack
aws s3 --recursive --profile=rnr-bdp rm s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/

