#! /bin/sh

# init parameters #######
echo "Which .py modelet?"
read modelet
echo "Which station?"
read station
echo "Which parameter?"
read parameter
echo "How many times?"
read times
declare -i times
#########################

for ((i=0; i<=times; i++))
do
	python $script.py $station $times
done


wait
echo "The files have run"

