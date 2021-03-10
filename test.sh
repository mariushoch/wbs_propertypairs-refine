#!/bin/sh

if ! result="$(python3 refine.py test.wbs_propertypairs.csv /dev/stdout)"; then
	exit 1
fi

keptLines=7

[ "$(echo "$result" | grep -c ',to-be-kept,')" -lt "$keptLines" ] && echo "Failure: Missing line!" && exit 1
[ "$(echo "$result" | grep -c ',to-be-kept,')" -gt "$keptLines" ] && echo "Failure: More to-be-kept lines than expected!" && exit 1
echo "$result" | grep -q ',to-be-removed,' && echo "Failure: Extra line!" && exit 1
[ "$(echo "$result" | wc -l)" -ne "$((keptLines + 1))" ] && echo "Unexpected output line count!" && exit 1

echo "Success!"
exit 0
