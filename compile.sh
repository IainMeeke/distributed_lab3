#!/bin/sh



for i in {1..25}
do
   echo $a
   ruby client.rb &
done