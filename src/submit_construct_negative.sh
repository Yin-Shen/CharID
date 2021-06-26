#!/bin/bash
if [ $1 == Local ]
  then
    bash $2"/src/"construct_negative_local.sh $2 $3
elif [ $1 == LSF ]
  then
    bash $2"/src/"construct_negative_lsf.sh $2 $4
else [ $1 == PBS ]
    bash $2"/src/"construct_negative_pbs.sh $2 $5
fi

