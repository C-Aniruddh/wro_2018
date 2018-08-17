import actuators.dynamixel.servo_functions as servos
import config

if __name__ == '__main__':
    # Open port
    print("Opening Port!")
    if servos.enable_port():
        # take Id for the Servos as Input

        botId = int(input("Enter The Bot ID(Enter -1 to Quit):"))
        print("Enabling Torque on the Servo Id [%d]", botId)
        servos.enable_bot(botId)
        while True:
            exAngle = int(input("Enter the Servo Angle(0-1023)"))
            servos.set_speed(botId, config.servoSpeed)
            servos.write_pos(botId, exAngle)
            print("------------------------------------------------------------------")
        print("\n[+] Disabling")
        servos.closePort(port_num)
