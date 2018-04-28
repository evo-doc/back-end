#!/bin/bash

# template: run.bash "script to run" "output file" "parameters to pass to the script"
# example: bash ./run.bash "python3 example.py" "out_example.txt" "param1 param2 param3"

if (($# != 3)); then
    echo "template: run.bash \"script to run\" \"output file\" \"parameters to pass to the script\""
    exit 1
fi

($1 $3) > $2
