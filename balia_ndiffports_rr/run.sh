#!/bin/sh 
COUNTER=0
while [ "$COUNTER" -lt 50 ]
do
   sudo python /home/vagrant/minitopo/runner.py -t topo -x iperf_scenario
   echo $COUNTER
   echo "Finish"
   IPERFCOUNTER=IPERF_${COUNTER}
   mv iperf.log0 $IPERFCOUNTER
   COUNTER=`expr $COUNTER + 1`
done
