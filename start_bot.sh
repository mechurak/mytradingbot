#!/bin/sh
PWD=`pwd`

export PYTHONPATH=$PYTHONPATH:$PWD/mytradingbot

# nohup: Ignore logout(?)
nohup python ./mytradingbot/main.py &

