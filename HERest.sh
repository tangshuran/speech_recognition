#!/bin/sh
#Script to apply HERest n times
#
if [ $# != 7 ]
then
echo "Error - Incorrect number of arguments"
echo "Syntax - $0 name_start_dir name_end_dir #iterations config-file phones.mlf train.scp monophones"
exit 1
fi
startdir=$1
enddir=$2
n=$3
config=$4
phones=$5
train=$6
mono=$7
mkdir _hmm0
cp $startdir/* _hmm0
for (( i = 1 ; i <= $n; i++ ))
do
echo $i
mkdir _hmm$i
HERest -C $config -I $phones -t 250.0 150.0 1000 -S $train -H _hmm`expr $i - 1`/macros -H _hmm`expr $i - 1`/hmmdefs  -M _hmm$i $mono
rm -r _hmm`expr $i - 1`
done
mkdir $enddir
mv _hmm$n/* $enddir
rmdir _hmm$n

