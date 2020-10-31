#!/bin/bash

HOME=$(dirname ${BASH_SOURCE[0]})/..
VERIDOC=$HOME/src/veridoc/veridoc.py
VLOGFILE=$HOME/examples/rtl/lib/gates/generic/OAI22.sv

echo "python3 $VERIDOC -s $VLOGFILE > $HOME/examples/example1.html"
