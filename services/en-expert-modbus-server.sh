#!/bin/sh
# /etc/init.d/en-expert-modbus-server

case "$1" in
start)
  echo "Starting en-expert modbus server service"
  /usr/local/bin/python3 /opt/en-expert/modbus-server/main.py &
  ;;
stop)
  echo "Stopping en-expert modbus server service"
  pkill -f /opt/en-expert/modbus-server/main.py
  ;;
restart)
  echo "Restarting en-expert modbus server service"
  pkill -f /opt/en-expert/modbus-server/main.py
  /usr/local/bin/python3 /opt/en-expert/modbus-server/main.py &
  ;;
*)
  echo "Usage: /etc/init.d/en-expert-modbus-server {start|stop|restart}"
  exit 1
  ;;
esac

exit 0
