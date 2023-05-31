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
   ./install.sh
   ````

## Manual Install Notes

1. Copy the files on the device (Suggestion: /opt/en-expert/modbus-server/)
   Rename the config.example.yml file to config.yml and edit it to match your setup.
2. Make sure python version 3.5.3 is installed
    ```bash
    curl -s update.resiot.io/extra/python3/resiot_gw_x2_x4_x7_update_python_to_353.sh | bash
3. Update pip with (stay below version 21):
    ```bash
    python3 -m pip install --upgrade pip
   ```
4. Install the requirements with pip3 install -r requirements.txt
5. Run both scripts
   ```bash
   python3 main.py
   ```
   and let it run a few minutes to see if it works.
7. If it works, you can copy the service files to /etc/init.d/en-expert-modbus-server
   /etc/init.d/en-expert-modbus-updater and make them executable
   ```bash
   chmod +x /etc/init.d/en-expert-modbus-updater
   chmod +x /etc/init.d/en-expert-modbus-server
   ```
   and enable it with
   ```bash
   update-rc.d /etc/init.d/en-expert-modbus-updater defaults
   update-rc.d /etc/init.d/en-expert-modbus-server defaults
   ```
   The defaults option sets the script to start up in runlevels 2, 3, 4, and 5 (which are the usual multi-user
   runlevels), and to shut down in runlevels 0, 1, and 6 (halt, single-user mode, and reboot, respectively).)
8. Start the service and check if it works (maybe also perform a power cut) <br>
   Remember: Since we have no `service`, `systemctl` or other System V wrapper , we have to use the init.d script
   directly
   ```bash
   service /etc/init.d/en-expert-modbus-server restart
   service /etc/init.d/en-expert-modbus-updater restart
   ```
   ```bash
   service /etc/init.d/en-expert-modbus-server status
   service /etc/init.d/en-expert-modbus-updater status
   ```
   ```bash
   service /etc/init.d/en-expert-modbus-updater stop
   service /etc/init.d/en-expert-modbus-server stop
   ```

NOTE: Log files are located in /var/log/en-expert-modbus.server.log and /var/log/en-expert-modbus.updater.log