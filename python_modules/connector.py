# this module connects with aurduino board and exchanges data

# Python Code (arduino_receiver.py)
import serial
import time

commands = {
    "open": ["open", "allow", "come", "permission"],
    "update_status": ["update", "parking", "status", "available"],
    "close_gate": ["close", "down", "block"]
}

class PortReader:
    def __init__(self, port):
        self.connected = False
        try:
            self.port_reader = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Allow time for connection to establish
            self.connected = True
        except serial.SerialException as e:
            print(f"Error opening port {port}: {e}")
            self.port_reader = None

    def send_command(self, comand):
        #print(f"comand received; {com}")
        if self.port_reader is None:
            print("Serial port not initialized.")
            return

        #comand = [key for key, value in commands.items() if any(word in value for word in com.strip())]

        if comand:
            command_string = comand + '\n'
            self.port_reader.write(command_string.encode('utf-8'))
            print(f"Sending command: {command_string.strip()}")
            time.sleep(17)
            # Wait for and receive confirmation from Arduino
            confirmation = self.read_port()
            if confirmation:
                print(f"Arduino confirmation: {confirmation}")
            else:
                print("No confirmation received from Arduino.")
        else:
            print("No matching command found.")


    def read_port(self, timeout=2, retries=3):
        start_time = time.time()
        for _ in range(retries):
            if self.port_reader.in_waiting > 0:
                self.port_reader.reset_input_buffer()
                time.sleep(1)
                raw_data = self.port_reader.readline()
                print(f"Raw data received: {raw_data}")
                self.port_reader.reset_input_buffer()
                return raw_data.decode("utf-8").rstrip()
            time.sleep(1)  # Small delay between retries
            if time.time() - start_time > timeout:
                break  # timeout.
        return None

    def read_last_port_message(self, timeout=2, retries=3):
        start_time = time.time()
        for _ in range(retries):
            if self.port_reader.in_waiting > 0:
                # Read all available data
                raw_data = self.port_reader.read(self.port_reader.in_waiting)
                print(f"Raw data received: {raw_data}")
                self.port_reader.reset_input_buffer()
                # Split the raw data into individual messages if needed
                messages = raw_data.decode("utf-8").split("\n")
                if messages:
                    return messages[-1].rstrip()  # Return the last message
            time.sleep(1)  # Small delay between retries
            if time.time() - start_time > timeout:
                break  # timeout.
        return None


if __name__ == "__main__":

    read = PortReader('COM6')
    while True:


            #read.send_command(com)
            msg =read.read_port()
            print(msg)