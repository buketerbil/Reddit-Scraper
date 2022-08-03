FROM python:3.9.7

RUN apt-get update && apt-get install -y wget
RUN apt-get -y update &&\
    apt install -y wget &&\
    apt install -y gnupg &&\
    # adding trusting keys to get apps for repositories
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -  &&\
    # Adding Google Chrome 
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get -y update &&\
    # installing Google Chrome 
    apt-get install -y google-chrome-stable &&\
    # installing unzip 
    apt-get install -yqq unzip &&\
    # install the latest release of ChromeDriver
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    # installing unzip and using it to unzip temporary directory for Chromedriver
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ 

#setting display port in order to not get crashes
ENV DISPLAY=:99

COPY . .
RUN pip install -r requirements.txt
CMD ["python", "justry.py"]



# FROM ubuntu:18.04
# # apt update ensures all packages and dependencies are at their latest version but doesnt update existing packages that have been installed
# # apt install actually uses the updated packages so its recommended to run apt-install before apt-update
# # && apt-get install -y gnupg2 wget curl
# RUN apt-get -y update && apt-get -y upgrade 
# #download and install chrome
# RUN apt-get install chromium-browser -y
# RUN apt-get install wget -y 
# RUN apt-get install python3-pip -y && pip3 install --no-cache-dir --upgrade pip
# RUN wget -q http://launchpadlibrarian.net/614041843/chromium-chromedriver_103.0.5060.134-0ubuntu0.18.04.1_arm64.deb
# # Installing Unzip
# RUN dpkg -i chromium-chromedriver_103.0.5060.134-0ubuntu0.18.04.1_arm64.deb

# # Download the Chrome Driver

# # Unzip the Chrome Driver into /usr/local/bin directory


# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# RUN pip install .
# CMD ["python", "justry.py"]






# FROM selenium/standalone-chrome
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# CMD ["python", "justry.py"]
