#!/usr/bin/env python3

from datetime import datetime, timedelta
import utils.time_utils as time_utils
import yaml
import sys

#----- check the python version because this assumes we use ordered dictionaries
assert sys.version_info >= (3, 6), "Requires python > 3.6"

#----- load and parse yaml file
yamlpath = '../test/testinput/s3_source.yaml'
f = open(yamlpath)
config_dict = yaml.safe_load(f)
f.close()

# read date range
dr = time_utils.get_date_range_from_dict(config_dict.get('date_range'))
# read cycling interval in seconds
cycling_interval = config_dict.get('cycling_interval')
# read source info
sources = config_dict.get('source')

#----- cycle through the date range
while not(dr.at_end()):
  current_cycle = dr.current
  print(current_cycle)
  dr.increment(seconds = cycling_interval)
  #----- cycle through the sources
  for source in sources.items():
    source_name = source[1].get('name')
    print(f"using {source_name} at time {current_cycle}")

print('at the end of the time loop')


