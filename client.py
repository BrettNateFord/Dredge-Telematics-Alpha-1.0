import socket
import matplotlib.pyplot as plt
import re

#**************************************************************************************************#
#                                       Data Visualization                                         #
#***************************************************************************************************
# Initialize plot for fuel and oil levels received from the server
plt.ion()  # Turn on interactive mode for live updates
fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('Level')
plt.title('Real-time Fuel and Oil Levels Plot')
plt.show()

# Set up TCP connection to the server
HOST = '127.0.0.1'  # Loopback IP address
PORT = 65432  # Port to connect to

# Create lists to store fuel and oil levels for plotting
fuel_levels = []
oil_levels = []

#**************************************************************************************************#
#                               TCP Connection and Data Display                                    #
#***************************************************************************************************

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect the client socket to the server
    client_socket.connect((HOST, PORT))

    while True:
        data = client_socket.recv(1024)  # Receive data from the server
        
        if not data:
            break
        
        decoded_data = data.decode('utf-8')
        print(f"Received data: {decoded_data}")
        
        # Check if the received data contains fuel and oil levels information
        if 'Fuel Level' in decoded_data and 'Oil Level' in decoded_data:
            try:
                fuel_level = float(re.search(r'\d+\.\d+', decoded_data.split('Fuel Level: ')[1]).group())
                oil_level = float(re.search(r'\d+\.\d+', decoded_data.split('Oil Level: ')[1]).group())
                
                fuel_levels.append(fuel_level)
                oil_levels.append(oil_level)
                
                # Plot fuel and oil levels in real-time
                ax.plot(fuel_levels, label='Fuel Level')
                ax.plot(oil_levels, label='Oil Level')
                ax.legend()
                plt.pause(0.01)  # Small pause to update the plot
            except AttributeError:
                pass  # Ignore non-numeric data
