# Email IP on Boot (for debain systems)

I've been setting up various headless RaspberryPI recently, and every time I've had to check the router's configuration page for the IP address that the Pi is using. This is obviously not the most efficient way to go about things, so I wrote a script for it.

This python (3) script runs 'ip route list' and then emails the relevant information to whoever you fancy, just edit the config.ini file to add some recipients.

At the moment, only gmail is supported, but I may add another line to the configuration file so you can define a custom SMTP server.

### Running it on boot

After you've flashed a fresh Raspberry Pi card, transfer the script over to the filesystem. You can put it wherever you like, I put mine inside /etc/ but I'm not sure if that's the best idea.

Make sure the script is executable by running 'sudo chmod 775 email\_ip.py'.

Once you've done that you can edit your rc.local file by adding '/path/to/script/email\_ip.py' before 'exit 0'.

Then plug in your Raspberry Pi and wait for your IP address to arrive in your email!
