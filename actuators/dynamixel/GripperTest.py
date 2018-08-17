import actuators.dynamixel.super_servo_functions as super

if __name__ == "__main__":
    super.init()
    super.enable(8)
    while True:
        input("press any key to grab the block")
        super.gripEnable()
        input("press any key to release the block")
        super.gripDisable()
