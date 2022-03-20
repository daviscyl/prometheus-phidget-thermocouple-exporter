FROM python:3

WORKDIR /usr/src/app

# install phidget22 library for linux (https://www.phidgets.com/docs/OS_-_Linux#Root)
RUN curl -fsSL https://www.phidgets.com/downloads/setup_linux -o phidget_linux_setup.sh
RUN bash -e phidget_linux_setup.sh
RUN apt install -y libusb-1.0-0 libphidget22

# copy usb rules for phidget devices so usb can be opened non-root
# delete it because in the docker image I'm root???
# COPY 99-libphidget22.rules /etc/udev/rules.d/

# install python wrapper for phidget22 library
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy over the main script and run it
COPY prometheus-phidget-thermocouple-exporter.py ./
CMD [ "python3", "./prometheus-phidget-thermocouple-exporter.py" ]

EXPOSE 9981