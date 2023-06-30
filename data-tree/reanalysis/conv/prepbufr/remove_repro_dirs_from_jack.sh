startdate=$(date -I -d "1990-01-01") || exit -1
enddate=$(date -I -d "2021-01-01")     || exit -1

d="$startdate"
while [ "$d" != "$enddate" ]; do 
  echo $d
  Y=$(date -d $d +%Y)
  M=$(date -d $d +%m)
  str="aws s3 --recursive  --profile=rnr-bdp rm s3://noaa-reanalyses-pds/observations/reanalysis/conv/prepbufr/$Y/$M/prepbufr_reprocessed_v1.0/"
  echo $str
  $str

  d=$(date -I -d "$d + 1 month")
done

d="$startdate"
while [ "$d" != "$enddate" ]; do
  echo $d
  Y=$(date -d $d +%Y)
  M=$(date -d $d +%m)
  str="aws s3 --recursive  --profile=rnr-bdp rm s3://noaa-reanalyses-pds/observations/reanalysis/conv/prepbufr/$Y/$M/prepqc/"
  echo $str
  $str

  d=$(date -I -d "$d + 1 month")
done

