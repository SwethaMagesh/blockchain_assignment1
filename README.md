# Blockchain Project
Build Own discrete-event simulator for a P2P cryptocurrency network.
A discrete-event simulator maintains an ”event-queue” from which the earliest event is executed. This event may create further future events which get added to the queue. For example, an event in which one node ”sends a block” to connected peers will create future events of ”receive block” at its peers.

---
**Run Simulation**: 

- Parameters in either of the below forms
  
 `--peers PEERS --slow SLOW --low LOW --txninterval TXNINTERVAL --blockinterval BLOCKINTERVAL`

 `--n PEERS --z0 SLOW --z1 LOW --Ttx TXNINTERVAL --I BLOCKINTERVAL`

```
bash runsimulation.sh -n 10 -z0 0.3 -z1 0.4 -Ttx 2 -I 60
python3 main.py -n 10 -z0 0.5 -z1 0.5 -Ttx 10 -I 60 -a1 0.4 -a2 0.1 >

```
Output: Chain visualisations are found in fig folder while logs of arrival and creation of blocks, transactions are in the logs folder.
**NOTE: Networkx libraries for generation of graph gets stuck sometimes. If the script takes more time, just rerun the command again.**

**Requirements:**
Install the following python dependencies
```
simpy
networkx
matplotlib
```

---
