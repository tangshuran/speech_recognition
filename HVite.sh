#!/bin/sh
#Script to apply HVite and HResults
#
if [ $# != 7 ]
then
echo "Error - Incorrect number of arguments"
echo "Syntax - $0 hmm_dir test.scp name_output.mlf wordnet dict monophones_with_sp reference.mlf "
exit 1
fi
hmmdir=$1
test=$2
output=$3
grammar=$4
dict=$5
monophones=$6
reference=$7
HVite -H $hmmdir/macros -H $hmmdir/hmmdefs -S $test -l '*' -i $output -w $grammar -p 0.0 -s 5.0 $dict $monophones
HResults -I $reference $monophones $output






