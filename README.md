# blockchain_assignment1
Build Own discrete-event simulator for a P2P cryptocurrency
network.
A discrete-event simulator maintains an ”event-queue” from which the earliest event is executed. This event may create further future events which get added to the queue. For example,
an event in which one node ”sends a block” to connected peers will create future events of ”receive block” at its peers.

- Tasks
1. slow and slow cpu peers
2. Exponential parameter
    - 4 marks implementation 
    - 2 marks why exponential (report)
3. Transaction: TxnID: IDx pays IDy C coins
4. Connected graph (3 and 6 peers)
    - 4 marks
5. Latencies
    - 12 marks
    - justification - 2marks
6. Loopless forwardingg
    - 4marks
7. PoW = block struct, creation, validation, mining, propagation, Tk
    - 20 marks
    - Fork resolution - 8 marks
8. Tree file
    - 10 marks

---
visualisation 
    - 12 marks
    - insight - 8 marks

---
Command line
n, z, Ttx, Tk, edges,  invalid_txn_prob, invalid_block_prob, zeta, adv, alpha