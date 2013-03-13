#!/bin/sh
lines=`grep -rne hline $1 | cut -d: -f2`
echo $lines
LINES=($lines)
start=${LINES[1]}
startRange="3,$start""d"
echo $startRange
sed -i '' "$startRange" $1

lines=`grep -rne hline $1 | cut -d: -f2`
LINES=($lines)
end=${LINES[0]}
endRange="$end,100""d"
echo $endRange
sed -i '' "$endRange" $1
