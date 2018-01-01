#!/bin/sh
PWD=`pwd`

export PYTHONPATH=$PYTHONPATH:$PWD/mytradingbot:$PWD/mytradingbot/slack

# nohup: Ignore logout(?)
nohup python ./mytradingbot/slack/run.py &
