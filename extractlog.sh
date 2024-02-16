# for loop for P1 to Pn
n="$1"
for ((i=1;i<=n;i++))
do
    grep  "^[0-9. ]*P$i" blockchain.log > ./logs/P$i.log
done