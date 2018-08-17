import actuators.dynamixel.servo_functions as servo

if __name__ == "__main__":
    servo.enable_port()
    print("Enabling Torque on All Servos !!")
    servo.enable_bot(6)
    servo.enable_bot(7)
    servo.enable_bot(11)
    servo.enable_bot(16)
    servo.enable_bot(9)
    servo.enable_bot(8)

    while True:
        id = int(raw_input("Enter Motor ID:"))

        tq = servo.read_load(id, 1)
        Torque_precent = 0.0

        if (tq < 1023):
            Torque_precent = float(tq) / 1023 * 100
        else:
            Torque_precent = float(tq - 1023) / 1023 * 100

        print("Torque Precentage:", Torque_precent)
