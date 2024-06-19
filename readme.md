# Speedometer
Speedometer is an application that is designed to measure internet speed
autonomously during the day.

![GitHub Repo stars](https://img.shields.io/github/stars/lucas-watkins/speedometer)⠀⠀
![GitHub forks](https://img.shields.io/github/forks/lucas-watkins/speedometer)

![Screenshot](https://i.ibb.co/N2vZ1J4/Screenshot-2024-06-19-at-15-50-25-Speedometer-Dashboard.png)

# Setup
I would recomend downloading all the code onto a raspberry pi and then making a
cron job to run main.py on startup.
```
# Clone repo
git clone https://github.com/lucas-watkins/speedometer.git

# Make cron job
crontab -e

# Append "@reboot python3 /path/to/code/main.py" to the file
# (Without Quotes)

# Reboot raspberry pi
sudo reboot
```
Now after this, you should be able to visit your pi's address in
browser and look at the charts. 