# Jack W. has compiled some merged repro and original satwinds in his dorectory s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/
# this moves them to s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/

aws s3 --recursive --profile=rnr-bdp cp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/ s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/
aws s3 --recursive --profile=rnr-bdp cp observations/reanalysis/amv/merged/ s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/
aws s3 --recursive --profile=rnr-bdp cp s3://noaa-reanalyses-pds/observations/reprocessed-from-jack/amv/MERG/README s3://noaa-reanalyses-pds/observations/reanalysis/amv/merged/

