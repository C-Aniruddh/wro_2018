import actuators.dynamixel.servo_functions as s

if __name__ == "__main__":
    s.enable_port()
    while True:
        id = input("Enter Bot ID:")
        print(s.read_torque(id))
