#!/bin/sh
# /etc/init.d/en-expert-modbus-updater

case "$1" in
start)
  echo "Starting en-expert modbus updater service"
  /usr/local/bin/python3 /opt/en-expert/modbus-updater/main.py
  ;;
stop)
  echo "Stopping en-expert modbus updater service"
  pkill -f /opt/en-expert/modbus-updater/main.py
  ;;
restart)
  echo "Restarting en-expert modbus updater service"
  pkill -f /opt/en-expert/modbus-updater/main.py
  /usr/local/bin/python3 /opt/en-expert/modbus-updater/main.py &
  ;;
*)
  echo "Usage: /etc/init.d/en-expert-modbus-updater {start|stop|restart}"
  exit 1
  ;;
esac

exit 0
