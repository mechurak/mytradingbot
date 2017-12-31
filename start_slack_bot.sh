#!/bin/sh
PWD=`pwd`

export PYTHONPATH=$PYTHONPATH:$PWD/mytradingbot:$PWD/mytradingbot/slack

python ./mytradingbot/slack/run.py &
