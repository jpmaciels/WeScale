import serial
import time
import requests

# Initialize serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port as necessary
time.sleep(2)  # Wait for the serial connection to initialize
recibo = ""

def read_from_arduino():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            return line

def send_to_arduino(message):
    ser.write((message + '\n').encode('utf-8'))

def get_api_response():
    url = "http://18.221.251.191:3000/user/1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_received_number(number):
    global recibo
    if number == "10":
        api_response = get_api_response()
        if api_response:
            nome_produto = api_response.get("nome_produto", "unknown").lower()
            id_produto = api_response.get("id", "unknown")
            valor_produto = api_response.get("valor_produto", "unknown")
            recibo += f"{nome_produto}_{id_produto}_{valor_produto},"
            return f"{nome_produto}_{id_produto}_{valor_produto}"
        else:
            return "error_fetching_data"
    elif number == "20":
        return f"{recibo[:-1]}"
    else:
        return f"Number received: {number}"

def main():
    try:
        while True:
            # Read the number from Arduino
            received_number = read_from_arduino()
            print(f"Received from Arduino: {received_number}")
            
            # Process the number and create a response string
            response_string = process_received_number(received_number)
            
            # Send the response back to Arduino
            send_to_arduino(response_string)
            print(f"Sent to Arduino: {response_string}")

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        ser.close()
        print("Serial connection closed")

if __name__ == "__main__":
    main()
