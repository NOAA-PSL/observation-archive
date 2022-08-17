#!/usr/bin/env python3

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

#----- create source clients
print('Opening aws resources')
source_clients = []
for source in sources.items():
  source_clients.append(boto3.Session().client('s3'))
#----- create destination session
destination_session = boto3.Session(profile_name=destination.get('credential_profile'))
destination_bucket = destination_session.resource('s3').Bucket(destination["bucket"])
destination_fn_template = destination.get('path')+destination["file_template"]["prefix"]+destination["file_template"]["root"]+destination["file_template"]["suffix"]
print('...Done')

#----- open log files
print('Opening loggers')
dtg = datetime.now().strftime('%Y%m%d%H%M%S')
logger_success = open(config_dict["logging"]["success"].format(dtg=dtg),'wt')
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
    # construct source filename
    fn_template = source["file_template"]["prefix"]+source["file_template"]["root"]+source["file_template"]["suffix"]
    source_dict = {"Bucket" : source["bucket"], "Key" : current_cycle.strftime(source["key"]+fn_template)}
    # if source file exists, then copy
    try:
      destination_bucket.copy( source_dict, destination_key)
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == "404":
        # log that the file is missing and try next source
        logger_missing[si].write("s3://{}/{}\n".format(source_dict["Bucket"], source_dict["Key"]));
        continue
      else:
        # something else went wrong
        raise
    else:
      # log success message
      logger_success.write("s3://{}/{} -> s3://{}/{}\n".format(source_dict["Bucket"], source_dict["Key"], destination["bucket"], destination_key))
  dr.increment(seconds = cycling_interval)
print('done with the time loop')

#----- close logging files
print('closing loggers')
logger_success.close()
for l in logger_missing:
  l.close()
print('at the end')

