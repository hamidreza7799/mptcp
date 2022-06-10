#!/bin/sh 
COUNTER=0
while [ "$COUNTER" -lt 50 ]
do
   mprun -t topo -x iperf_senario
   IPERFCOUNTER=IPERF_${COUNTER}
   mv iperf.log0 $IPERFCOUNTER
   COUNTER=`expr $COUNTER + 1`
done