# blockchain_assignment1
Build Own discrete-event simulator for a P2P cryptocurrency network.
A discrete-event simulator maintains an ”event-queue” from which the earliest event is executed. This event may create further future events which get added to the queue. For example, an event in which one node ”sends a block” to connected peers will create future events of ”receive block” at its peers.

---
Run Simulation : 
Parameters Help
 --peers PEERS --slow SLOW --low LOW --txninterval TXNINTERVAL --blockinterval BLOCKINTERVAL
 OR
 --n PEERS --z0 SLOW --z1 LOW --Ttx TXNINTERVAL --I BLOCKINTERVAL
 
```
bash runsimulation.sh -n 10 -z0 0.3 -z1 0.4 -Ttx 2 -I 60
```

---
