#!/bin/bash

# Step 1: Create two files in /etc/openvpn/ with the provided content
echo -e '#!/bin/bash\necho "nameserver 194.151.228.34" > /etc/resolv.conf\necho "nameserver 194.151.228.18" >> /etc/resolv.conf' >/etc/openvpn/update-resolv-conf-down.sh

echo -e '#!/bin/bash\necho "nameserver 8.8.8.8" > /etc/resolv.conf\necho "nameserver 8.8.4.4" >> /etc/resolv.conf' >/etc/openvpn/update-resolv-conf-up.sh

# Step 2: Make both scripts executable
chmod +x /etc/openvpn/update-resolv-conf-down.sh
chmod +x /etc/openvpn/update-resolv-conf-up.sh

# Step 3: Find the file that starts with 'ExControl' and add lines to it
conf_file=$(find /etc/openvpn -type f -name 'ExControl*')

# Also, it's assumed that the <ca> tag is in the file. If it isn't, or there are multiple <ca> tags, this may not work as expected.
sed -i '/<ca>/i script-security 2\nup /etc/openvpn/update-resolv-conf-up.sh\ndown /etc/openvpn/update-resolv-conf-down.sh' "$conf_file"

# Step 4: Restart the OpenVPN service
# This should be enabled if we have a newer version -> not supported in 2.4.12
#openvpn --config "$conf_file" --check-config
