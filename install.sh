#!/bin/bash
# Function to compare version numbers
function version_ge() { test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"; }

# Check Python version
# Check if Python3 is installed
if ! command -v python3 &>/dev/null; then
  echo "Python3 could not be found. Installing ..."
  curl -s update.resiot.io/extra/python3/resiot_gw_x2_x4_x7_update_python_to_353.sh | bash
fi

python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
if version_ge $python_version 3.5; then
  echo "Python version is $python_version. OK"
else
  echo "Python is version $python_version. Python 3.5 or later is required. Updating ..."
  curl -s update.resiot.io/extra/python3/resiot_gw_x2_x4_x7_update_python_to_353.sh | bash
fi

# Check pip version
pip_version=$(pip3 --version 2>&1 | cut -d' ' -f2)
if version_ge $pip_version 20; then
  echo "pip version is $pip_version. OK"
else
  echo "pip version is $pip_version. pip 20.0 or later is required. Updating ..."
  python3 -m pip install --upgrade pip
fi

echo "Installing dependencies"
pip3 install -r requirements.txt
mkdir -p /opt/en-expert

echo "Copying data"
cp -r server/* /opt/en-expert/modbus-server
cp -r updater/* /opt/en-expert/modbus-updater
cp services/en-expert-modbus-server.sh /etc/init.d/en-expert-modbus-server.sh
cp services/en-expert-modbus-updater.sh /etc/init.d/en-expert-modbus-updater.sh

echo "Changing permissions"
chmod +x /etc/init.d/en-expert-modbus-server.sh
chmod +x /etc/init.d/en-expert-modbus-updater.sh

echo "Installing services"
update-rc.d en-expert-modbus-updater.sh defaults
update-rc.d en-expert-modbus-server.sh defaults
/etc/init.d/en-expert-modbus-server.sh restart
/etc/init.d/en-expert-modbus-updater.sh restart

echo "Finished. OK"
