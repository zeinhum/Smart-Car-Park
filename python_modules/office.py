import time
from connector import PortReader
#from test import PortReader
from vehicle_detection import DetectVehicle
from audiomode import controlstation


class ParkControler:
    def __init__(self):
        self.registered_vehicles = []  # Simulates database for registered number plates
        self.port = PortReader('COM6')

        self.allow_commands = ["allow", "come", "coming", "grant", "access", "open", "register"]
        self.quit_commands = ["quit", "stop", "terminate"]
        self.arriving_vehicle = None  # Track the current arriving vehicle

    def registration(self):
        """Registers a new number plate if it's not already registered."""
        if self.arriving_vehicle and self.arriving_vehicle not in self.registered_vehicles:
            self.registered_vehicles.append(self.arriving_vehicle)
            print(f"Vehicle {self.arriving_vehicle} registered successfully.")
            return True
        else:
            print(f"Vehicle {self.arriving_vehicle} is already registered.")
            return False

    def allow_vehicle(self):
        """Checks if the detected vehicle is registered and should be allowed in."""
        vehicle = DetectVehicle()
        self.arriving_vehicle = vehicle.plate_number()  # Always fetch a new plate number
        print(f"Detected vehicle: {self.arriving_vehicle}")

        if self.arriving_vehicle in self.registered_vehicles:
            print("Vehicle allowed.")
            return True
        else:
            print("Vehicle not registered.")
            return False

    def is_spot_available(self):
        """Checks if a parking spot is available by reading the port."""
        try:
            port_message = self.port.read_port()

            return port_message.strip().lower() == 'available'
        except Exception as e:
            print(f"Error reading port: {e}")
            return False

    def main_run(self):
        """Controls the parking system."""
        while True:
            if self.allow_vehicle():
                if self.is_spot_available():
                    controlstation.speak("The gate is opening.")
                    self.port.send_command('open')
                else:
                    controlstation.speak("Sorry! The parking is full.")
                    return
            else:
                controlstation.speak("Sorry! The vehicle is not registered, I am not allowed to open the gate.")
                command = controlstation.listener()

                if command:
                    command_words = command.split()
                    if any(word in command_words for word in self.allow_commands):
                        controlstation.speak("Sure! Please hold on.")
                        self.registration()
                        controlstation.speak("Almost done, I just need to scan the number plate once again")
                    if any(word in command_words for word in self.quit_commands):
                        controlstation.speak("Stopping the system.")
                        return

            time.sleep(2)  # Allow process to rest before restarting


if __name__ == "__main__":
    office = ParkControler()
    while True:
        office.main_run()

