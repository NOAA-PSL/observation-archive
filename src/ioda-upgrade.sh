#!/bin/sh

set -x

export blddir=/scratch2/BMC/gsienkf/Wei.Huang/jedi/debug/build
export LD_LIBRARY_PATH=${blddir}/lib:$LD_LIBRARY_PATH

echo "file-name: $1"
echo "out-name: $2"

./ioda-upgrade-v2-to-v3.x $1 $2 ObsSpace.yaml
