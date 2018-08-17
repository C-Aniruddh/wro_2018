import actuators.dynamixel.super_servo_functions as super

if __name__=="__main__":
    super.init()
    super.disable(6)        #Base Parrallelogram 
    super.disable(7)
    super.disable(16)
    super.disable(11)
    super.disable(9)
    super.disable(8)    # Gripper


    while True:
        # angle0 = constants.transform2StandardAngles(super.getAngle(6),0)
        # angle1 = constants.transform2StandardAngles(super.getAngle(7),1)
        # angle2=constants.transform2StandardAngles(super.getAngle(16),2)
        # angle3= constants.transform2StandardAngles(super.getAngle(11),3)
        # angle4=constants.transform2StandardAngles(super.getAngle(9),4)
        # angle5=constants.transform2StandardAngles(super.getAngle(8),5)

        angle0i = super.getAngle(6)
        angle1i = super.getAngle(7)
        angle2i=super.getAngle(16)
        angle3i= super.getAngle(11)
        angle4i=super.getAngle(9)
        angle5i=super.getAngle(8)

        # angle0=int(angle0)
        # angle1=int(angle1)
        # angle2=int(angle2)
        # angle3=int(angle3)
        # angle4=int(angle4)
        # angle5=int(angle5)

        angle0i=int(angle0i)
        angle1i=int(angle1i)
        angle2i=int(angle2i)
        angle3i=int(angle3i)
        angle4i=int(angle4i)
        angle5i=int(angle5i)

        # print(angle0,angle1,angle2,angle3,angle4,angle5)
        # print(angle0,angle1,angle2,angle3,angle4,angle5 )
        print(angle0i,angle1i,angle2i,angle3i,angle4i,angle5i )
