#!/bin/bash

pkill zebra

ip next flush

ip link add dummy1 type dummy
ip link add dummy2 type dummy

ip link set dummy1 up
ip link set dummy2 up

ip addr add 1.0.0.1 dev dummy1
ip addr add 2.0.0.1 dev dummy2
ip addr add 2001::1/127 dev dummy2

ip next add id 1 via 1.0.0.1 dev dummy1
ip next add id 11 dev dummy1
ip next add id 22 dev dummy2
ip next add id 11111 blackhole

ip -6 next add id 226 dev dummy2
ip -6 next add id 116 via 2001::0 dev dummy2

ip next add id 1001 group 1/11
ip next add id 2001 group 1/226
ip next add id 2002 group 116/226

ip ro add 9.9.9.0/24 nhid 11111
ip ro add 1.1.1.0/24 nhid 1
ip ro add 2.2.2.0/24 nhid 1001
ip ro add 6.6.6.0/24 nhid 2001

ip -6 ro add 6666::0/127 nhid 2002


/usr/lib/frr/zebra --log stdout --log-level debug &> zebra_output.log &

echo "Sleeping for startup..."
sleep 5
echo "Starting pytest..."
pytest

pkill zebra

ip next flush
