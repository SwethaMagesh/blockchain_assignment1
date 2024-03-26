n=100
a1=0.3
a2=0
Ttx=10
I=30

# # checking a2=0, 0.3
a2=0.3
a1=0.3
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 6 > outputs/30_3
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 20 > outputs/30_2
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 60 > outputs/30_1

# similar for a1=0.4
a1=0.4
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 6 > outputs/40_3
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 20 > outputs/40_2
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 60 > outputs/40_1

# similar for a1=0.5
a1=0.5
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 6 > outputs/50_3
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 20 > outputs/50_2
bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I 60 > outputs/50_1



# save figs into output
# rm -rf outputs/a1_30_a2_0
# mkdir -p outputs/a1_30_a2_0
# cp figs/* outputs/a1_30_a2_0/


# bash runsimulation.sh -n $n -a1 $a1 -a2 0.3 -Ttx $Ttx -I $I > outputs/a1_30_a2_30.log
# save figs into output


# # change a1 = .4 and a2 = 0 and .3

a1=0.4

# bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I $I > outputs/a1_40_a2_0.log
# save figs into output

# bash runsimulation.sh -n $n -a1 $a1 -a2 0.3 -Ttx $Ttx -I $I > outputs/a1_40_a2_30.log
# save figs into output



# a1=.5
# bash runsimulation.sh -n $n -a1 $a1 -a2 0 -Ttx $Ttx -I $I > outputs/a1_50_a2_0.log
# save figs into output



# bash runsimulation.sh -n $n -a1 $a1 -a2 0.3 -Ttx $Ttx -I $I > outputs/a1_50_a2_30.log
