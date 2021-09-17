#!/bin/bash
cat ./sample.txt | while read line
do
  eval "./csux_req.sh --url $line >> sample1.txt"
done
