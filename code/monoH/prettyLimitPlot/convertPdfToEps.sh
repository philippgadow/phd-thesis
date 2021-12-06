#!/bin/bash
if [ !'-z $1' ] ; then
  STRING=${1}
fi

for i in `ls *${STRING}*.eps`
do
  echo "epstopdf $i"
  epstopdf $i
done

