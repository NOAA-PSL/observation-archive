#!/usr/bin/env python3

from datetime import datetime
import utils.time_utils as time_utils
import utils.file_utils as file_utils
import yaml
import sys
import boto3
import botocore
import subprocess
import os

#----- check the python version because this assumes we use ordered dictionaries
assert sys.version_info >= (3, 6), "Requires python > 3.6"

#----- load and parse yaml file
#yamlpath = '../test/testinput/s3_source.yaml'
assert len(sys.argv) == 2, "Config file not specified. Required calling sequence: s3-copy.py <config.yaml>"
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
#move_flag = config_dict.get('remove source file','false').lower() == 'true'
move_flag = config_dict.get('remove source file','false')

#----- create source clients
print('Opening aws resources')
destination_bucket = boto3.Session(profile_name=destination.get('credential_profile')).resource('s3').Bucket(destination["bucket"])
destination_fn_template = destination.get('path')+destination["file_template"]["prefix"]+destination["file_template"]["root"]+destination["file_template"]["suffix"]
destionation_file_template = destination["file_template"]["prefix"]+destination["file_template"]["root"]+destination["file_template"]["suffix"]
source_buckets = []
for source in sources.values():
  source_buckets.append( boto3.Session(profile_name=source["credential_profile"]).resource('s3').Bucket(source["bucket"]))
print('...Done')

#----- open log files
print('Opening loggers')
dtg = datetime.now().strftime('%Y%m%d%H%M%S')
logger_present = open(config_dict["logging"]["present"].format(dtg=dtg),'wt')
logger_success = open(config_dict["logging"]["success"].format(dtg=dtg),'wt')
if (move_flag):
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
  destination_filename = current_cycle.strftime(destionation_file_template)
  print(current_cycle)

  #----- cycle through the sources
  si = -1
  for source in sources.values():
    si = si + 1
    # construct source filename
    fn_template = source["file_template"]["prefix"]+source["file_template"]["root"]+source["file_template"]["suffix"]
    source_filename = current_cycle.strftime(fn_template)
    source_dict = {"Bucket" : source["bucket"], "Key" : current_cycle.strftime(source["key"]+fn_template)}

    # check first if destination exists and it is the same as source
    try: md5destination = destination_bucket.Object(destination_key).e_tag[1 :-1]
    except: pass
    else: #destination file exists
      try: md5source = source_buckets[si].Object(source_dict["Key"]).e_tag[1 :-1]
      except: pass
      else: #source file exists
        if (md5source == md5destination):
          # log that this file is present 
          logger_present.write("s3://{}/{} == s3://{}/{}\n".format(source_dict["Bucket"], source_dict["Key"], destination["bucket"], destination_key))
          print(f" present {si}")
          # skip to next, no need to copy identical file
          break

    # if source file exists but the destiantion doesnt, then copy
    try:
        #download file, convert to ioda v3, upload to destination
        v2_file = "/iodav2/" + source_filename
        source_buckets[si].download_file(source_dict["Key"], v2_file)
        subprocess.run(["ioda-upgrade-v2-to-v3.x", v2_file, destination_filename, "ObsSpace.yaml"])
        destination_bucket.upload_file(destination_filename, destination_key)

        #remove locally downloaded files 
        os.remove(v2_file)
        os.remove(destination_filename)
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == "404":
        # log that the file is missing and try next source
        logger_missing[si].write("s3://{}/{}\n".format(source_dict["Bucket"], source_dict["Key"]));
        print(f" missing {si}")
        continue
      else:
        # something else went wrong
        raise
    else:
      # log success message
      logger_success.write("s3://{}/{} -> s3://{}/{}\n".format(source_dict["Bucket"], source_dict["Key"], destination["bucket"], destination_key))
      print(f" copy from {si}")

      # remove source file if needed
      if (move_flag):
        source_buckets[si].Object(source_dict["Key"]).delete()
        logger_remove.write("rm s3://{}/{}\n".format(source_dict["Bucket"], source_dict["Key"]))
        print(f" remove from {si}")
      break
  # increment time counter
  dr.increment(seconds = cycling_interval)
print('done with the time loop')

#----- close logging files
print('closing loggers')
logger_success.close()
logger_present.close()
if (move_flag):
  logger_remove.close()
for l in logger_missing:
  l.close()
print('at the end')

