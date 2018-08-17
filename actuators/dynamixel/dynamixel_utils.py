# Servo Angles Transformation Functions
def transform2ServoAngles(angle, angleIndex):
    CompoundAngle = 0

    if angleIndex == 0:
        CompoundAngle = (((angle - 141) / (-0.29)) + 0)  # Increase in Gear Ratio
    if angleIndex == 1:
        CompoundAngle = (((angle - 13) / (-0.29)) + 496) * 2  # Reduction in Gear Ratio
    if angleIndex == 2:
        CompoundAngle = ((angle / (-0.29)) + 192)
    if angleIndex == 3:
        CompoundAngle = ((angle - 41) / (-0.29))
    if angleIndex == 4:
        CompoundAngle = (angle / (0.29))
    if angleIndex == 5:
        CompoundAngle = (angle / (0.29))
    return int(CompoundAngle) % 1023


def transform2StandardAngles(angle, angleIndex):
    if angleIndex == 0:
        return (((angle - 0) * 0.29) * (-1)) + 141  # Increase in Gear Ratio
    if angleIndex == 1:
        return ((((angle - 496) * 0.29) * (-1)) + 13) / 2  # Reduction in Gear Ratio
    elif angleIndex == 2:
        return ((angle - 192) * 0.29) * (-1)
    elif angleIndex == 3:
        return (angle * 0.29) * (-1) + 41
    elif angleIndex == 4:
        return angle * 0.29
    elif angleIndex == 5:
        return angle * 0.29
