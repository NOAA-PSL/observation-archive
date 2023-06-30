=== 20230630* ===
frolovsa moved missing files from jack using 199107.from_jack.prepbufr.yaml 200401-200406.from_jack.prepbufr.yaml 199704.from_jack.prepbufr.yaml
using 4a7700e2

=== 20230622 ===
frolovsa moved files with QC mark from jack using 1990-2010.from_jack.prepbufr.yaml and 4a7700e2

=== 20230601194653 ===
frolovsa renamed prefur files using 9464200f and 1990-2020.clean_bucket.prepfur.yaml 

=== 20220823151121 and 20220823194132 ===
first upload for 1990-2021 was done in two stages 1990-2000 2000-2021 using a version of the check-in 
1990-2020.clean_bucket.yaml
there was also a version of 1990s.clean_bucket.yaml but it was removed

=== 20220830160612 ===
frolovsa discovered that 20000101-20100501 used a wrong data feed during the upload. 
we used 'gefsv13_reanalysis-md5/' for the first and second data feed when the intention was to use
(1) gefsv13_reanalysis-md5.sherrie.fredrick and (2) gefsv13_reanalysis-md5
to correct frolovsa ran 
1) remove_wrong_2000-2010.sh
2) 20000101-20100501.clean_bucket.cfsr_backfill.yaml with (94d8fca)

=== 20220831153238 ===
frolovsa backfilled missing files using 1990-2020.clean_bucket.missing.yaml from gefsv13_reanalysis-md5.missing 

=== Fri Sep  9 14:57:58 UTC 2022 ===
renamed 
s3://noaa-reanalyses-pds/observations/reanalysis/conv/gefs-prepbufr/ to 
s3://noaa-reanalyses-pds/observations/reanalysis/conv/prepbufr/



