import socket
import time
import random

#**************************************************************************************************#
#                               NMEA 0183 Data Component Simulators                                #
#***************************************************************************************************
def encode_nmea0183_tuple(data_tuple):
    # Format the tuple elements into an NMEA 0183 string
    nmea_string = f"${','.join(map(str, data_tuple))}*"
    checksum = 0
    for char in nmea_string[1:]:
        checksum ^= ord(char)
    nmea_string += f"{checksum:02X}"
    return nmea_string

def generate_nmea0183_data():
    # Combined functions, all will be used per tick
    
    def generate_gpgga_data():
        # Mock function to generate NMEA 0183 $GPGGA data
        
        # Sample data for different parameters
        time_utc = '{:02d}{:02d}{:02d}'.format(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        latitude = '{:02d}{:09.6f}'.format(random.randint(-90, 90), random.uniform(0, 59))
        longitude = '{:03d}{:09.6f}'.format(random.randint(-180, 180), random.uniform(0, 59))
        fix_quality = random.randint(0, 2)  # 0: No fix, 1: GPS fix, 2: Differential GPS fix
        satellites = random.randint(0, 12)  # Number of satellites being tracked
        hdop = round(random.uniform(0.5, 5.0), 1)  # Horizontal Dilution of Precision
        altitude = round(random.uniform(-100, 1000), 1)  # Altitude in meters above sea level
        geoid_height = round(random.uniform(-50, 50), 1)  # Geoidal separation in meters
        
        # Create the $GPGGA string
        gpgga_sentence = f"$GPGGA,{time_utc},{latitude},N,{longitude},E,{fix_quality},{satellites},{hdop},{altitude},M,{geoid_height},M,,"
        checksum = 0
        for char in gpgga_sentence[1:]:
            checksum ^= ord(char)
        gpgga_sentence += f"*{checksum:02X}"
        
        return gpgga_sentence

    def generate_gprmc_data():
        # Mock function to generate NMEA 0183 $GPRMC data
        
        # Sample data for different parameters
        time_utc = '{:02d}{:02d}{:02d}'.format(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        status = 'A'  # 'A' for active, 'V' for void
        latitude = '{:02d}{:09.6f}'.format(random.randint(-90, 90), random.uniform(0, 59))
        longitude = '{:03d}{:09.6f}'.format(random.randint(-180, 180), random.uniform(0, 59))
        speed_over_ground = round(random.uniform(0, 100), 2)  # Speed over ground in knots
        true_course = round(random.uniform(0, 360), 2)  # True course in degrees
        date_utc = '{:02d}{:02d}{:02d}'.format(random.randint(1, 31), random.randint(1, 12), random.randint(0, 99))
        magnetic_variation = round(random.uniform(0, 180), 2)  # Magnetic variation in degrees
        
        # Create the $GPRMC string
        gprmc_sentence = f"$GPRMC,{time_utc},{status},{latitude},N,{longitude},E,{speed_over_ground},{true_course},{date_utc},{magnetic_variation},E*"
        checksum = 0
        for char in gprmc_sentence[1:]:
            checksum ^= ord(char)
        gprmc_sentence += f"{checksum:02X}"
        
        return gprmc_sentence #return encoded data

    def generate_sddbt_data():
        # Mock function to generate NMEA 0183 $SDDBT data
        
        # Sample data for different parameters
        depth_feet = round(random.uniform(0, 100), 2)  # Depth below transducer in feet
        depth_meters = round(depth_feet * 0.3048, 2)  # Convert feet to meters
        
        # Create the $SDDBT string
        sddbt_sentence = f"$SDDBT,{depth_feet},f,{depth_meters},M*"
        checksum = 0
        for char in sddbt_sentence[1:]:
            checksum ^= ord(char)
        sddbt_sentence += f"{checksum:02X}"
        
        return sddbt_sentence #return encoded data

    def generate_sdmtw_data():
        # Mock function to generate NMEA 0183 $SDMTW data
        
        # Sample data for sea surface temperature in Celsius
        sea_temp_celsius = round(random.uniform(0, 30), 2)
        
        # Create the $SDMTW string
        sdmtw_sentence = f"$SDMTW,{sea_temp_celsius},C*"
        checksum = 0
        for char in sdmtw_sentence[1:]:
            checksum ^= ord(char)
        sdmtw_sentence += f"{checksum:02X}"
        
        return sdmtw_sentence
    
    gpgga = generate_gpgga_data()  # GPS Fix Data
    gprmc = generate_gprmc_data()  # Recommended Minimum Specific GPS/Transit Data
    sddbt = generate_sddbt_data()  # Depth below transducer
    sdmtw = generate_sdmtw_data()  # Water temperature
    
    return gpgga, gprmc, sddbt, sdmtw

#**************************************************************************************************#
#                               NMEA 2000 Data Component Simulators                                #
#***************************************************************************************************
def generate_nmea2000_data():
    # Generate simulated NMEA 2000 data with common PGN codes found in dredge applications
    pgn = random.randint(100, 200)
    # Simulate some example data based on the PGN
    if pgn == 100:  # Example: Engine Parameters
        engine_rpm = random.randint(600, 3000)  # RPM between 600 and 3000
        engine_temp = random.uniform(50.0, 120.0)  # Engine temperature between 50.0 and 120.0 degrees Celsius
        return f"NMEA 2000 PGN: {pgn}, Engine RPM: {engine_rpm}, Engine Temperature: {engine_temp} C".encode('utf-8')
    elif pgn == 130311:  # Example: Environmental Parameters
        water_depth = random.uniform(0.0, 50.0)  # Water depth in meters
        water_temp = random.uniform(5.0, 30.0)  # Water temperature in Celsius
        return f"NMEA 2000 PGN: {pgn}, Water Depth: {water_depth}m, Water Temperature: {water_temp}C".encode('utf-8')
    else:
        return f"NMEA 2000 PGN: {pgn}, Data: Example Data".encode('utf-8')
    
#**************************************************************************************************#
#                                     Socket Connection                                            #
#***************************************************************************************************
# Server configuration
HOST = '127.0.0.1'  # Loopback IP address
PORT = 65432  # Port to listen on

fuel_decay_lower = 2.7  #Random fuel decay lower limit
fuel_decay_upper = 3.8  #Random fuel decay upper limit
initial_fuel = 100 #We will use 100 as an easy to estimate starting capacity


# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen()
    print('Server is listening...')
    
    # Accept incoming connection
    conn, addr = server_socket.accept()
    with conn:
        print(f'Connected by {addr}')
        
        while True:
            gpgga, gprmc, sddbt, sdmtw = generate_nmea0183_data()  # Generate NMEA 0183 data
            nmea2000_data = generate_nmea2000_data()  # Generate NMEA 2000 data
            for x in [gpgga, gprmc, sddbt, sdmtw]:
                x = x.encode('utf-8')
                conn.sendall(x)  # Send generated NMEA 0183 data to the client
                time.sleep(.25)
            time.sleep(.25) # Simulate sending data at intervals
            conn.sendall(nmea2000_data)  # Send generated NMEA 2000 data to the client
            # Simulate sending data at intervals
            
            # Simulate dredge fuel and oil data and send it to the client
            initial_fuel = initial_fuel - round(random.uniform(fuel_decay_lower, fuel_decay_upper), 2)  # Fuel level percentage
            oil_level = round(random.uniform(31.0, 51.0), 2)  # Oil level in liters
            
            dredge_data = f"Fuel Level: {initial_fuel}%, Oil Level: {oil_level}L".encode('utf-8')
            conn.sendall(dredge_data)  # Send dredge data to the client
            time.sleep(1)  # Simulate sending data at intervals
