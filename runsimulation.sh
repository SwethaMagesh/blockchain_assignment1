#!/bin/bash
mkdir -p figs
mkdir -p logs
rm -rf ./figs/*
rm -rf ./logs/*

while [[ "$#" -gt 0 ]]
  do
    case $1 in
      -n|--peers) n="$2"; shift;;
      -z0|--slow) z0="$2"; shift;;
      -z1|--low) z1="$2"; shift;;
      -Ttx|--txninterval) Ttx="$2"; shift;;
      -I|--blockinterval) I="$2"; shift;;
    esac
    shift
done

cd src
python3 main.py -n $n -z0 $z0 -z1 $z1 -Ttx $Ttx -I $I -a1 0.3 -a2 0.3