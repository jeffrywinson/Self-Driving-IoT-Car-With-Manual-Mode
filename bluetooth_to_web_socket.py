import asyncio
import serial
import websockets
import json
import sys

# --- CONFIGURATION ---
# IMPORTANT: Replace this with the COM port you found in Step 2.
# For Windows: e.g., "COM3", "COM4"
# For macOS/Linux: e.g., "/dev/tty.ESP32_Car-SPP"
SERIAL_PORT = "COM4"  # <--- CHANGE THIS!

# WebSocket server configuration
HOST = "localhost"
PORT = 8765

# --- SCRIPT LOGIC ---

# A set to keep track of all connected web clients
connected_clients = set()

async def register_client(websocket):
    """Adds a new client to the set of connected clients."""
    print(f"New client connected: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print(f"Client disconnected: {websocket.remote_address}")
        connected_clients.remove(websocket)

async def broadcast_to_clients(message):
    """Sends a message to all connected web clients."""
    if connected_clients:
        # Use asyncio.gather to send messages to all clients concurrently
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

async def read_from_serial():
    """Continuously reads data from the serial port and broadcasts it."""
    print(f"Attempting to connect to serial port: {SERIAL_PORT}")
    while True:
        try:
            # The 'with' statement ensures the serial port is closed properly
            with serial.Serial(SERIAL_PORT, 115200, timeout=1) as ser:
                print(f"Successfully connected to {SERIAL_PORT}. Reading data...")
                while True:
                    # Read one line of data from the ESP32
                    line = ser.readline()
                    if line:
                        try:
                            # Decode from bytes to string and remove whitespace
                            message = line.decode('utf-8').strip()
                            
                            # Validate that it's proper JSON before sending
                            json.loads(message) 
                            
                            print(f"Received from ESP32: {message}")
                            await broadcast_to_clients(message)
                        except (UnicodeDecodeError, json.JSONDecodeError) as e:
                            print(f"Warning: Could not decode or parse line: {line}, Error: {e}")
        except serial.SerialException as e:
            print(f"Error: Could not open serial port {SERIAL_PORT}. Is the device paired and correct port selected?")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5) # Wait before retrying

async def main():
    """Starts the WebSocket server and the serial reader task."""
    print(f"Starting WebSocket server on ws://{HOST}:{PORT}")
    
    # Create a task to read from the serial port in the background
    serial_task = asyncio.create_task(read_from_serial())
    
    # Start the WebSocket server to listen for browser connections
    async with websockets.serve(register_client, HOST, PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

