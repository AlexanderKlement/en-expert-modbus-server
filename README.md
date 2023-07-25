# EnExpert Modbus Server + Updater (for ResIOT Gateway x2)

These scripts are providing a ModBusTCP Slave that can be updated via an external Database.

## Install via Installer (recommended):

1. Get latest release (replace RELEASE)
   ````bash
   curl -LJO https://github.com/AlexanderKlement/en-expert-modbus-service/archive/refs/tags/RELEASE.tar.gz
   ````
2. Extract the archive
   ````bash
   tar xzvf en-expert-modbus-service-RELEASE.tar.gz
   ````
3. Run the installer
   ````bash
   cd en-expert-modbus-service-RELEASE
   chmod +x install.sh
   ./install.sh
   ````

NOTE#1: Log files are located in /var/log/en-expert-modbus.server.log and /var/log/en-expert-modbus.updater.log
NOTE#2: Manual install is deprecated and will not be maintained anymore. 