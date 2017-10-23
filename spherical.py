import numpy as np
import math


class Spherical(object):
    '''
    (x - a)^2 + (y - b)^2 = r^2



    so circles have a centerpoint (a,b) and a radius (r)
    '''
    def __init__(self, focal_length, depth, height):
        self.height = height
        self.r = abs(self.focal_length_to_radius(focal_length))
        self.fl = focal_length
        self.a = None
        self.b = 0
        self.depth = depth


    def set_x_offset(self, x_offset):
        if self.fl < 0:  # We wanna bounce off the right side of the circle
            self.a = x_offset - self.r
        else: # we wanna bounce off the left side?
            self.a = x_offset + self.r

        print "SETTING OFFSET"
        print "offset, radius, a:", x_offset, self.r, self.a


    def prop(self, eqns):
        a = self.a
        # b = self.b
        r = self.r

        result_ms = []
        result_bs = []
        result_xs = []
        result_ys = []
        result_freqs = []
        result_colors = []

        for eq in eqns:
            m, b, old_x, old_y, freq = eq

            if m == 0:
                '''
                The special case is super easy
                (x - a)^2 + (y - b)^2 = r^2
                (x - a) = sqrt(r^2 - (y - b)^2)
                x = sqrt(r^2 - (y - b)^2) + a
                x = sqrt(r^2 - y^2) + a
                '''
                y0 = b
                x0 = math.sqrt(self.r * self.r - y0 * y0) + self.a

            else:
                # Newton's Method
                # y0 = b
                # for i in xrange(1):
                #     fy = a * y0 * y0 - (1.0 / m) * y0 + c + b / m
                #     fydot = 2 * a * y0 - (1.0 / m)
                #     y1 = y0 - fy / fydot
                #     y0 = y1

                # x0 = a * y0 * y0 + c

                x0 = self.a + self.r
                for i in xrange(10):
                    # fx = (-m * m - 1) * x0 * x0 + (2 * a + 2 * b * m) * x0 + b * b - a * a + r * r
                    # fxdot = 2 * (-m * m - 1) * x0 + (2 * a + 2 * b * m)
                    fx = (m * m + 1) * x0 * x0 + (2 * b * m - 2 * a) * x0 + b * b + a * a - r * r
                    fxdot = 2 * (m * m + 1) * x0 + (2 * b * m - 2 * a)
                    x1 = x0 - fx / fxdot
                    if x1 - x0 == 0:
                        break
                    x0 = x1

                y0 = m * x0 + b

            # Okay we've found the intercept, let's reflect.
            # First step is to find the slope of the reflected line
            slope_inverse = -y0 / math.sqrt(self.r * self.r - y0 * y0)
            # print "SI", x0, y0, slope_inverse

            if slope_inverse == 0:
                # Another special case: the parabola is perfectly vertical here
                # All we gotta do is reflect off a vertical line, which amounts
                # to flipping the sign of the slope
                final_m = -m

            else:
                M1 = 1 / slope_inverse
                M2 = m
                M3 = (M1 * M1 * M2 + 2 * M1 - M2) / (1 + 2 * M1 * M2 - M1 * M1)
                final_m = M3

            # Great, just plug in the slope and a know point on the line
            # To find the y intercept
            final_b = y0 - final_m * x0

            result_ms.append(final_m)
            result_bs.append(final_b)
            result_xs.append(x0)
            result_ys.append(y0)
            result_freqs.append(freq)

        return np.array(zip(
            result_ms, result_bs, result_xs, result_ys, result_freqs))

    def focal_length_to_radius(self, focal_length):
        return focal_length * 2

    def __str__(self):
        return "Spherical: x = Math.sqrt(Math.pow({}, 2) - Math.pow(y, 2)) + {} : {}".format(self.r, self.a, self.height)

