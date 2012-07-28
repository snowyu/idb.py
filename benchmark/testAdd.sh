#!/bin/sh
#===================================================================
s_time()	# (c) RHReepe. Returns string (HHMMSS)
#===================================================================
{
    date +%H%M%S
}
#===================================================================
s_interval()	# (c) RHReepe. Returns a time difference (HH:MM:SS)
#===================================================================
# Arg_1 = start_time (Format - See s_time)
# Arg_2 = stop_time  (Format - See s_time)
{
    h1=`echo $1 | cut -c1-2`	# Get Start Hour
    m1=`echo $1 | cut -c3-4`	# Get Start Minute
    s1=`echo $1 | cut -c5-6`	# Get Start Second
    h2=`echo $2 | cut -c1-2`	# Get Stop Hour
    m2=`echo $2 | cut -c3-4`	# Get Stop Minute
    s2=`echo $2 | cut -c5-6`	# Get Stop Second
    s3=`expr $s2 - $s1`		# Calculate Second Difference
    if [ $s3 -lt 0 ]		# Test for Negative Seconds
    then
	s3=`expr $s3 + 60`	# If yes - add one minute...
	m1=`expr $m1 + 1`		# ... and to subtractor
    fi
    m3=`expr $m2 - $m1`		# Calculate Minute Difference
    if [ $m3 -lt 0 ]		# Test for Negative Minutes
    then
	m3=`expr $m3 + 60`	# If yes - add one hour...
	h1=`expr $h1 + 1`		# ... and to subtractor
    fi
    h3=`expr $h2 - $h1`		# Calculate Hour Difference
    if [ $h3 -lt 0 ]		# Test for Negative Hours
    then
	h3=`expr $h3 + 24`	# If yes - add one day
    fi
    for number in $h3 $m3 $s3	# Loop through numbers...
    do
	if [ $number -lt 10 ]	# If number is single digit...
	then
	    echo "0$number" # ... add leading zero
	else
	    echo "$number"  # ... else - don't
	fi
    done
    echo ""			# Terminate the string
}

#echo `s_time`
TESTPROG='testRedis'
LOOP=1000
REPEAT=3
COUNT=3

if [ $# -lt 1 ]
then
  echo Usage: Bechmark the specified python program
  echo "test.sh TestProg [Loop Repeat Count]"
  echo "default: test testRedis $LOOP $REPEAT $COUNT"
  exit
else
  TESTPROG=$1
fi

if [ $# -ge 2 ]
then
  LOOP=$2
fi
if [ $# -ge 3 ]
then
  REPEAT=$3
fi
if [ $# -ge 4 ]
then
  COUNT=$4
fi

echo benchmark the add key/value, run $TESTPROG loop $LOOP, repeat $REPEAT, total $COUNT
#echo clear DB first
#redis/redis-cli -p 3333 flushdb
#python -m timeit -s 'from '$TESTPROG' import a' -n 1 -r 1 'a.test_add()'
#DBCOUNT=$(redis/redis-cli -p 3333 dbsize)
#echo the total db record count: $DBCOUNT

I=0
TST=`s_time`
while [ $I -lt $COUNT ]
do
  I=$(( $I + 1 ))
  ST=`s_time`
  RESULT=$(python -m timeit -v -s 'from '$TESTPROG' import a' -n $LOOP -r $REPEAT 'a.test_add()')
  ET=`s_time`
  echo $I. $RESULT
  echo "running time(H M S):" `s_interval $ST $ET`
done
TET=`s_time`
echo "total running time(H M S):" `s_interval $TST $TET`
#echo $RESULT
#DBCOUNT=$(redis/redis-cli -p 3333 dbsize)
#echo the total db record count: $DBCOUNT

