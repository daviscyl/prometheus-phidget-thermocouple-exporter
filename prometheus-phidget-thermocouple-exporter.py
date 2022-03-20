from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.TemperatureSensor import *

from prometheus_client import start_http_server, Gauge

import traceback
import threading

# Create prometheus gauges
gauges = [
    Gauge('temperature_rpi_1_phidget_0_celcius', 'Description of gauge'),
    Gauge('temperature_rpi_1_phidget_1_celcius', 'Description of gauge'),
    Gauge('temperature_rpi_1_phidget_2_celcius', 'Description of gauge'),
    Gauge('temperature_rpi_1_phidget_3_celcius', 'Description of gauge')
]


# Declare event handlers

def onTemperatureChange(self, temperature):
    gauges[self.getChannel()].set(temperature)


def onAttach(self):
    print("Attach [" + str(self.getChannel()) + "]!")


def onDetach(self):
    print("Detach [" + str(self.getChannel()) + "]!")


def onError(self, code, description):
    print("Code [" + str(self.getChannel()) + "]: " +
          ErrorEventCode.getName(code))
    print("Description [" + str(self.getChannel()) + "]: " + str(description))
    print("----------")


if __name__ == '__main__':
    try:
        Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidgetlog.log")

        # Create Phidget channels
        temperatureSensor0 = TemperatureSensor()
        temperatureSensor1 = TemperatureSensor()
        temperatureSensor2 = TemperatureSensor()
        temperatureSensor3 = TemperatureSensor()

        # Set addressing parameters to specify which channel to open (if any)
        temperatureSensor0.setChannel(0)
        temperatureSensor1.setChannel(1)
        temperatureSensor2.setChannel(2)
        temperatureSensor3.setChannel(3)

        # Assign event handlers needed before calling open so that no events are missed.
        temperatureSensor0.setOnTemperatureChangeHandler(onTemperatureChange)
        temperatureSensor0.setOnAttachHandler(onAttach)
        temperatureSensor0.setOnDetachHandler(onDetach)
        temperatureSensor0.setOnErrorHandler(onError)

        temperatureSensor1.setOnTemperatureChangeHandler(onTemperatureChange)
        temperatureSensor1.setOnAttachHandler(onAttach)
        temperatureSensor1.setOnDetachHandler(onDetach)
        temperatureSensor1.setOnErrorHandler(onError)

        temperatureSensor2.setOnTemperatureChangeHandler(onTemperatureChange)
        temperatureSensor2.setOnAttachHandler(onAttach)
        temperatureSensor2.setOnDetachHandler(onDetach)
        temperatureSensor2.setOnErrorHandler(onError)

        temperatureSensor3.setOnTemperatureChangeHandler(onTemperatureChange)
        temperatureSensor3.setOnAttachHandler(onAttach)
        temperatureSensor3.setOnDetachHandler(onDetach)
        temperatureSensor3.setOnErrorHandler(onError)

        # Open your Phidgets and wait for attachment
        temperatureSensor0.openWaitForAttachment(5000)
        temperatureSensor1.openWaitForAttachment(5000)
        temperatureSensor2.openWaitForAttachment(5000)
        temperatureSensor3.openWaitForAttachment(5000)

        # Start up the server to expose the metrics.
        start_http_server(8000)
        threading.Event().wait()

    except PhidgetException as ex:
        # We will catch Phidget Exceptions here, and print the error informaiton.
        traceback.print_exc()
        print("")
        print("PhidgetException " + str(ex.code) +
              " (" + ex.description + "): " + ex.details)

    finally:
        # Close your Phidgets once the program is done.
        temperatureSensor0.close()
        temperatureSensor1.close()
        temperatureSensor2.close()
        temperatureSensor3.close()
