import os
import config

if os.name == 'nt':
    import msvcrt


    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)


    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

import actuators.dynamixel.cdynamixel as dynamixel

# Control table address
ADDR_MX_TORQUE_ENABLE = 24  # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36
ADDR_MX_GOAL_SPEED = 32
ADDR_MX_PRESENT_SPEED = 38
ADDR_MX_GOAL_ACCE = 73
ADDR_MX_TORQUE_CTRL = 70
ADDR_MX_GOAL_TORQUE = 71
ADDR_MX_PRESENT_LOAD = 40

ADDR_MX_TORQUE = 14

# Protocol version
PROTOCOL_VERSION = 1  # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE = 1000000
DEVICENAME = (config.ttyUSB_USB2DYNAMIXEL).encode('utf-8')  # Check which port is being used on your controller
# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 10  # Dynamixel moving status threshold

COMM_SUCCESS = 0  # Communication Success result value
COMM_TX_FAIL = -1001  # Communication Tx Failed

# Initialize PortHandler Structs
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
port_num = dynamixel.portHandler(DEVICENAME)

# Initialize PacketHandler Structs
dynamixel.packetHandler()

dxl_comm_result = COMM_TX_FAIL  # Communication result

dxl_error = 0  # Dynamixel error
dxl_present_position = 0  # Present position
dxl_present_speed = 0
dxl_present_load = 0


def enable_port():
    port_num = dynamixel.portHandler(DEVICENAME)

    # Open port
    if dynamixel.openPort(port_num):
        print("[] Succeeded to open the port!")
    else:
        print("[-] Failed to open the port!")
        quit()

    # Set port baudrate
    if dynamixel.setBaudRate(port_num, BAUDRATE):
        print("[] Succeeded to change the baudrate!")
    else:
        print("[-] Failed to change the baudrate!")
        quit()
    return True


def read_torque(ID):
    res = dynamixel.read2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_TORQUE)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
    return res


def enable_bot(ID):
    # Enable Dynamixel Torque
    dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
    else:
        print("[] Dynamixel has been successfully connected")


def write_pos(ID, final_pos):
    # Write goal position
    dynamixel.write2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_GOAL_POSITION, final_pos)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))


def read_pos(ID, prnt_enable):
    # Read present position
    dxl_present_position = dynamixel.read2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_PRESENT_POSITION)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

    if prnt_enable == 1:
        # print("[ID:%03d] PresPos:%03d" % (ID, dxl_present_position))
        print(dxl_present_position)
    return dxl_present_position


def set_speed(ID, speed):
    # Write goal speed
    dynamixel.write2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_GOAL_SPEED, speed)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))


def read_speed(ID, prnt_enable):
    # Read present speed
    dxl_present_speed = dynamixel.read2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_PRESENT_SPEED)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

    if prnt_enable == 1:
        # print("[ID:%03d] PresSpeed:%03d" % (ID, dxl_present_speed))
        pass

    return dxl_present_speed


def set_acc(ID, acce):
    # Write goal acce
    dynamixel.write2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_GOAL_ACCE, acce)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))


def read_load(ID, prnt_enable):
    # Read present load
    dxl_present_load = dynamixel.read2ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_PRESENT_LOAD)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

    if prnt_enable == 1:
        # print("[ID:%03d] PresLoad:%03d" % (ID, dxl_present_load))
        pass

    return dxl_present_load


def disable_bot(ID):
    # Disable Dynamixel Torque
    dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)


'''    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
'''

if __name__ == '__main__':
    # Open port
    if dynamixel.openPort(port_num):
        print("[] Succeeded to open the port!")
    else:
        print("[-] Failed to open the port!")
        quit()

    # Set port baudrate
    if dynamixel.setBaudRate(port_num, BAUDRATE):
        print("[] Succeeded to change the baudrate!")
    else:
        print("[-] Failed to change the baudrate!")
        quit()
    try:
        botid = input("Enter Bot Id: ")
        disable_bot(botid)
        # enable_bot(botid)
        #      enable_bot(4)
        #       enable_bot(6)
        # set_speed(botid,200)
        while True:
            # theta1 = input("Enter Theta1 value: ")
            # if theta0 >=300 or theta0 <=0:
            #   theta0 = 180
            # value0 = int(theta0/360 * 1023);
            # write_value(botid, theta1)
            read_pos(botid, 1)

        # theta1 = input("Enter Theta1 value: ")
        # theta2 = input("Enter Theta2 value: ")
        # theta0 = int(theta1)
        # if theta0 >=300 or theta0 <=0:
        # theta0 = 180

        # value0 = int(theta0/360 * 1023);

        # write_value(botid, value0)
        #     write_value(4, value1)
        #       write_value(6, value2)
        #
        while 1:
            continue
    except KeyboardInterrupt:
        print("\n[] Disabling")
        # disable_bot(2)
        # disable_bot(4)
        # disable_bot(6)

        # Close port
        dynamixel.closePort(port_num)
