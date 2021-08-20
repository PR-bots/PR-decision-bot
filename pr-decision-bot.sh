#!/bin/bash
AppName = "pr-decision-bot"
App="~/app/pr-decision-bot.py"

echo $1
echo $App

function killProcess() {
    NAME=$1
    echo $NAME
    PID=$(ps -e | grep $NAME | awk '{print $1}')
    echo "PID: $PID"
    kill -9 $PID
}

function start() {
    echo "start $AppName"
    nohup python -u $App > server.log 2>&1 &
}

function stop() {
    echo "stop $AppName"
    killProcess $AppName
}

function restart() {
    echo "restart $AppName"
    stop
    start
}

case "$1" in
    start )
        start
    stop )
        stop
    restart )
        restart
esac