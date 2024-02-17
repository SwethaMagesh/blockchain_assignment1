peers=50
slow=0.5
low=0.5
Ttx=0.02
blockinterval=0.02
simtime=1

python3 main.py -n $peers --slow $slow --low $low -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out.txt
mv scatter.png ./backup/scatter1.png
mv bar.png ./backup/bar1.png
mv fig2.png ./backup/fig2.png

# # checking peers
# # low & high to 10 and 100 remaining same
# python3 main.py -n 10 --slow $slow --low $low -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out_peerslow.txt
# mv scatter.png ./backup/scatter_peerslow.png
# mv bar.png ./backup/bar2_peerslow.png
# mv fig2.png ./backup/fig2_peerslow.png


# python3 main.py -n 100 --slow $slow --low $low -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out_peershigh.txt
# mv scatter.png ./backup/scatter_peershigh.png
# mv bar.png ./backup/bar2_peershigh.png
# mv fig2.png ./backup/fig2_peershigh.png

# checking Ttx
# low & high to 10 and 100 remaining same

# python3 main.py -n $peers --slow $slow --low $low -Ttx 0.1 --blockinterval $blockinterval -T $simtime > ./backup/out_Ttxlow.txt
# mv scatter.png ./backup/scatter_Ttxlow.png
# mv bar.png ./backup/bar2_Ttxlow.png
# mv fig2.png ./backup/fig2_Ttxlow.png
# mv fig3.png ./backup/fig3_Ttxlow.png

# python3 main.py -n $peers --slow $slow --low $low -Ttx 10 --blockinterval $blockinterval -T $simtime > ./backup/out_Ttxhigh.txt
# mv scatter.png ./backup/scatter_Ttxhigh.png
# mv bar.png ./backup/bar2_Ttxhigh.png
# mv fig2.png ./backup/fig2_Ttxhigh.png
# mv fig3.png ./backup/fig3_Ttxhigh.png

# checking blockinterval
# low & high to 1 and 100 with simtime 20 and 2000
# python3 main.py -n $peers --slow $slow --low $low -Ttx $Ttx --blockinterval 1 -T 40 > ./backup/out_blockintervallow.txt
# mv scatter.png ./backup/scatter_blockintervallow.png
# mv bar.png ./backup/bar2_blockintervallow.png
# mv fig2.png ./backup/fig2_blockintervallow.png
# mv fig3.png ./backup/fig3_blockintervallow.png

# python3 main.py -n $peers --slow $slow --low $low -Ttx $Ttx --blockinterval 100 -T 4000 > ./backup/out_blockintervalhigh.txt
# mv scatter.png ./backup/scatter_blockintervalhigh.png
# mv bar.png ./backup/bar2_blockintervalhigh.png
# mv fig2.png ./backup/fig2_blockintervalhigh.png
# mv fig3.png ./backup/fig3_blockintervalhigh.png

# # very low blockinterval at 0.1 with sim time 2 with slow at 0.7
# python3 main.py -n $peers --slow 0.7 --low $low -Ttx $Ttx --blockinterval 0.1 -T 4 > ./backup/out_blockintervalverylow.txt
# mv scatter.png ./backup/scatter_blockintervalverylow.png
# mv bar.png ./backup/bar2_blockintervalverylow.png
# mv fig2.png ./backup/fig2_blockintervalverylow.png
# mv fig3.png ./backup/fig3_blockintervalverylow.png


# checking slow 
# low & high to 0.1 and 0.9 with simtime 20 and 2000
# python3 main.py -n $peers --slow 0.1 --low $low -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out_slowlow.txt
# mv scatter.png ./backup/scatter_slowlow.png
# mv bar.png ./backup/bar2_slowlow.png
# mv fig2.png ./backup/fig2_slowlow.png
# mv fig3.png ./backup/fig3_slowlow.png

# python3 main.py -n $peers --slow 0.9 --low $low -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out_slowhigh.txt
# mv scatter.png ./backup/scatter_slowhigh.png
# mv bar.png ./backup/bar2_slowhigh.png
# mv fig2.png ./backup/fig2_slowhigh.png
# mv fig3.png ./backup/fig3_slowhigh.png


# checking cpu 
# low & high to 0.1 and 0.9 with simtime
# python3 main.py -n $peers --slow $slow --low 0.1 -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out_cpulow.txt
# mv scatter.png ./backup/scatter_cpulow.png
# mv bar.png ./backup/bar2_cpulow.png
# mv fig2.png ./backup/fig2_cpulow.png
# mv fig3.png ./backup/fig3_cpulow.png

# python3 main.py -n $peers --slow $slow --low 0.9 -Ttx $Ttx --blockinterval $blockinterval -T $simtime > ./backup/out_cpuhigh.txt
# mv scatter.png ./backup/scatter_cpuhigh.png
# mv bar.png ./backup/bar2_cpuhigh.png
# mv fig2.png ./backup/fig2_cpuhigh.png
# mv fig3.png ./backup/fig3_cpuhigh.png





