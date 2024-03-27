# Blockchain Project
Selfish mining setup in discrete-event simulator for a P2P cryptocurrency network.
A discrete-event simulator maintains an ”event-queue” from which the earliest event is executed. This event may create further future events which get added to the queue. For example, an event in which one node ”sends a block” to connected peers will create future events of ”receive block” at its peers.
- There are two independent selfish miners in the network, unaware of each other’s intentions. Remaining miners are completely honest. Honest miners follow the bitcoin rules and mine of the longest chain visible with the usual fork resolutions. 

- Half of the honest miners have slow link speed and the rest have fast link speed, while the selfish miners are always fast.

- We fix the fraction of hashing power of the selfish miners and assume that the remaining honest miners have equal fraction of hashing power, such that the sum of all is one.

**Assumption**
Peer 0 is adversary 1 
Peer 1 is adversary 2
Rest of n-2 peers are random honest peers

---
**Run Simulation**: 

- Parameters in either of the below forms
  
 `--peers PEERS --zeta1 ZETA1 --zeta2 ZETA2 --txninterval TXNINTERVAL --blockinterval BLOCKINTERVAL`

 `--n PEERS --a1 ZETA1 --a2 ZETA2 --Ttx TXNINTERVAL --I BLOCKINTERVAL`

```
bash runsimulation.sh -n 10 -a1 0.3 -a2 0.4 -Ttx 2 -I 60

```
Output: Chain visualisations are found in fig folder while logs of arrival and creation of blocks, transactions are in the logs folder.

Legend for fig folder:
Green - Honest visible chain, 
Pink  - Created by node and released
Red   - Created by node and not yet released
Blue  - Created by other nodes
---

**NOTE: Networkx libraries for generation of graph gets stuck sometimes. If the script takes more time, just rerun the command again.**

**Requirements:**
Install the following python dependencies
```
simpy
networkx
matplotlib
```

---
