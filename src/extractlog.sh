# for loop for P1 to Pn
n="$1"
for ((i=0;i<n;i++))
do
    grep  "^[0-9. ]*P$i" ../logs/blockchain.log > ../logs/P$i.log
done