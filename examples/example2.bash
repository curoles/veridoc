#!/bin/bash

HOME=$(dirname ${BASH_SOURCE[0]})/..
VERIDOC=$HOME/src/veridoc/veridoc.py
VF1=$HOME/examples/rtl/lib/gates/generic/OAI22.sv
VF2=$HOME/examples/rtl/lib/gates/cmos/Not.sv

echo "python3 $VERIDOC -s --inline -o $HOME/docs/example2.html $VF1 $VF2"
