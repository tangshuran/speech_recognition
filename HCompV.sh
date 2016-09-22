#!/bin/sh
#Script to apply HERest n times
#
if [ $# != 4 ]
then
echo "Error - Incorrect number of arguments"
echo "Syntax - $0 destination_dir config train.scp protoHMM"
exit 1
fi
destdir=$1
config=$2
train=$3
protoHMM=$4

mkdir $destdir
HCompV -C $config -f 0.01 -m -S $train -M $destdir $protoHMM

