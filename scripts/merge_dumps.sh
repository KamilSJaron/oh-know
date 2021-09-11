#!/bin/bash

echo -e $(basename $1 .dump)'\t'$(basename $2 .dump)'\t'$(basename $3 .dump)'\t'$(basename $4 .dump)'\t'$(basename $5 .dump)'\t'$(basename $6 .dump)'\t'$(basename $7 .dump)'\t'$(basename $8 .dump)

join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto $1 $2 | \
join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto - $3 | \
join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto - $4 | \
join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto - $5 | \
join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto - $6 | \
join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto - $7 | \
join -t $'\t' -a 1 -a 2 -1 1 -2 1 -e 0 -o auto - $8 
