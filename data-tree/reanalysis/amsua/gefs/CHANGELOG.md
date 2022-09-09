=== 20220826220644 ===
first upload was done for 1990-2021 using 1990-2020.clean_bucket.yaml

=== 20220830160754 ===
frolovsa discovered that 20000101-20100501 used a wrong data feed during the upload. 
we used 'gefsv13_reanalysis-md5/' for the first and second data feed when the intention was to use
(1) gefsv13_reanalysis-md5.sherrie.fredrick and (2) gefsv13_reanalysis-md5
to correct frolovsa ran 
1) remove_wrong_2000-2010.sh
2) 20000101-20100501.clean_bucket.cfsr_backfill.yaml with (94d8fca)

=== 20220902185429 ===
frolovsa copied 9 missing files from gefsv13_reanalysis-md5.missing/ using 1990-2020.clean_bucket.missing.yaml

