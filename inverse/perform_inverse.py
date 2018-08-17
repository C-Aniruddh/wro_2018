import math


class InverseKinematics:

    def solve(self, x, y, z):
        w1 = x  # x co-ordinate of end effector
        w2 = y  # y co-ordinate of end effector
        w3 = z  # z co-ordinate of end effector
        w4 = 0
        w5 = 0
        w6 = (-1)

        L1 = 4
        L2 = 16.3
        L3 = 7.8
        L4 = 3.7
        L5 = 15.5

        d1 = L1
        a2 = L2
        a3 = L3
        a4 = L4
        d5 = L5  # length of link 5

        q1 = math.atan2(w2, w1)

        c1 = math.cos(q1)
        s1 = math.sin(q1)

        q234 = math.atan2((-1) * (c1 * w4 + s1 * w5), (-1) * w6)
        # print"q234=",q234
        # print"servo1 angle =",q1*(180/math.pi)
        c234 = math.cos(q234)
        s234 = math.sin(q234)
        # print"s234=",s234
        b1 = c1 * w1 + s1 * w2 - a4 * (c234) + d5 * (s234)

        b2 = d1 - a4 * (s234) - d5 * (c234) - w3
        b = b1 ** 2 + b2 ** 2
        # print("b2=",b2)
        # print"b=",b

        z = (b - (a2 ** 2) - (a3 ** 2)) / (2 * a2 * a3)
        # print"z=",z

        if z > -1 and z < 1:

            q3 = (math.acos(z))
            # c3=math.cos(q3)
            c3 = z
            # print "c3",c3

            s3 = math.sin(q3)
            # print "s3",s3

            # print "first",((a2+a3*(c3))*b2 - a3*s3*b1)
            # print "second",((a2+a3*c3)*b1+a3*s3*b2)

            q2 = math.atan2(((a2 + a3 * (c3)) * b2 - a3 * (s3) * b1), ((a2 + a3 * c3) * b1 + a3 * s3 * b2))

            q4 = q234 - q2 - q3

            q5 = math.pi * (math.log(math.sqrt(w4 * w4 + w5 * w5 + w6 * w6)))
            # print("b1=",b1)
            # print("b2=",b2)
            # print"q234=",q234
            # print"z=",z
            # # print"c234=",c234
            # print"servo1 angle =",q1*(180/math.pi)
            # print"servo2 angle =",q2*(180/math.pi) + 90
            # print"servo3 angle =",q3*(180/math.pi) - 90
            # print"servo4 angle =",q4*(180/math.pi)
            # print"servo5 angle =",q5*(180/math.pi)

            q1 = q1 * (180 / math.pi)
            q2 = q2 * (180 / math.pi) + 90
            q3 = q3 * (180 / math.pi) - 90
            q4 = q4 * (180 / math.pi)
            q5 = q5 * (180 / math.pi)

            return q1, q2, q3, q4, q5, True

        else:
            print("this point is not in range")
            return 0, 0, 0, 0, 0, False
