#!/usr/bin/env python3

"""
s3-copy based script for copying all files within given source bucket to destinaton bucket
"""

from datetime import datetime
import utils.time_utils as time_utils
import utils.file_utils as file_utils
import yaml
import sys
import boto3
import botocore

#----- check the python version because this assumes we use ordered dictionaries
assert sys.version_info >= (3, 6), "Requires python > 3.6"

#----- load and parse yaml file
#yamlpath = '../test/testinput/s3_source.yaml'
assert len(sys.argv) == 2, "Config file not specified. Required calling sequence: s3-copy-bucket.py <config.yaml>"
yamlpath = sys.argv[1]
file_utils.is_valid_readable_file(yamlpath)
f = open(yamlpath)
config_dict = yaml.safe_load(f)
f.close()

# read date range
dr = time_utils.get_date_range_from_dict(config_dict.get('date_range'))
# read cycling interval in seconds
cycling_interval = config_dict.get('cycling_interval')
# read source info
sources = config_dict.get('source')
# read destination info
destination = config_dict.get('destination')
#read "move" flag
move_flag = config_dict.get('remove source file','false')
#----- create source clients
print('Opening aws resources')
destination_bucket = boto3.Session(profile_name=destination.get('credential_profile')).resource('s3').Bucket(destination["bucket"])
destination_fn_template = destination.get('path')
source_buckets = []
for source in sources.values():
  source_buckets.append( boto3.Session(profile_name=source["credential_profile"]).resource('s3').Bucket(source["bucket"]))
print('...Done')

#----- open log files
print('Opening loggers')
dtg = datetime.now().strftime('%Y%m%d%H%M%S')
logger_present = open(config_dict["logging"]["present"].format(dtg=dtg),'wt')
logger_success = open(config_dict["logging"]["success"].format(dtg=dtg),'wt')
if (move_flag != 'false'):
  logger_remove = open(config_dict["logging"]["remove"].format(dtg=dtg),'wt')
logger_missing = []
si = 0
for source in sources.values():
  sn = source["name"].replace(' ','_')
  logger_missing.append( open(config_dict["logging"]["missing"].format(dtg=dtg,source_num=si,source_name=sn), 'wt') )
  si = si + 1
print('...Done')

#----- cycle through the date range
print('Top of the time loop')
while not(dr.at_end()):
  #----- create destination path
  current_cycle = dr.current
  destination_key = current_cycle.strftime(destination_fn_template)
  print(current_cycle)

  #----- cycle through the sources
  si = -1
  for source in sources.values():
    si = si + 1
    # construct source name
    source_dict = {"Bucket" : source["bucket"], "Key" : current_cycle.strftime(source["key"])}
    #get files from source bucket 
    source_files = [f.key.split(source_dict["Key"])[1] for f in source_buckets[si].objects.filter(Prefix=source_dict["Key"]).all()]
    #loop through each file in bucket 
    for file in source_files:
        destination_file = destination_key + file
        source_dict_file = {"Bucket" : source_dict["Bucket"], "Key" : source_dict["Key"] + file}
        # check first if destination exists and it is the same as source
        try: md5destination = destination_bucket.Object(destination_file).e_tag[1 :-1]
        except: pass
        else: #destination file exists
            try: md5source = source_buckets[si].Object(source_dict_file["Key"]).e_tag[1 :-1]
            except: pass
            else: #source file exists
                if (md5source == md5destination):
                    # log that this file is present 
                    logger_present.write("s3://{}/{} == s3://{}/{}\n".format(source_dict_file["Bucket"], source_dict_file["Key"], destination["bucket"], destination_file))
                    print(f"{file} present {si}")
                    # skip to next, no need to copy identical file
                    continue

        # if source file exists but the destiantion doesnt, then copy
        try:
            destination_bucket.copy(source_dict_file, destination_file)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # log that the file is missing and try next source
                logger_missing[si].write("s3://{}/{}\n".format(source_dict_file["Bucket"], source_dict_file["Key"]));
                print(f"{file} missing {si}")
                continue
            else:
                # something else went wrong
                raise
        else:
            # log success message
            logger_success.write("s3://{}/{} -> s3://{}/{}\n".format(source_dict_file["Bucket"], source_dict_file["Key"], destination["bucket"], destination_file))
            print(f"{file} copy from {si}")

            # remove source file if needed
            if (move_flag != 'false'):
                source_buckets[si].Object(source_dict_file["Key"]).delete()
                logger_remove.write("rm s3://{}/{}\n".format(source_dict_file["Bucket"], source_dict_file["Key"]))
                print(f"{file} remove from {si}")
            continue

  # increment time counter
  dr.increment(seconds = cycling_interval)
print('done with the time loop')

#----- close logging files
print('closing loggers')
logger_success.close()
logger_present.close()
if (move_flag != 'false'):
  logger_remove.close()
for l in logger_missing:
  l.close()
print('at the end')

