import numpy as np


class Spherical(object):
    '''
    (x - a)^2 + (y - b)^2 = r^2

    so circles have a centerpoint (a,b) and a radius (r)
    '''
    def __init__(self, focal_length, depth):
        self.r = self.focal_length_to_radius(focal_length)
        self.a = None
        self.b = 0
        self.depth = depth

    def set_x_offset(self, x_offset):
        self.a = x_offset


    def prop(self, eqns):
        a = self.a
        b = self.b

        result_ms = []
        result_bs = []
        result_xs = []
        result_ys = []
        result_freqs = []
        result_colors = []

        for eq in eqns:
            m, b, old_x, old_y, freq = eq

            if m == 0:
                # The special case is super easy
                y0 = b
                x0 = a * y0 * y0 + c
            else:
                # Newton's Method
                y0 = b
                for i in xrange(1):
                    fy = a * y0 * y0 - (1.0 / m) * y0 + c + b / m
                    fydot = 2 * a * y0 - (1.0 / m)
                    y1 = y0 - fy / fydot
                    y0 = y1

                x0 = a * y0 * y0 + c

            # Okay we've found the intercept, let's reflect.
            # First step is to find the slope of the reflected line
            slope_inverse = 2 * a * y0
            if slope_inverse == 0:
                # Another special case: the parabola is perfectly vertical here
                # All we gotta do is reflect off a vertical line, which amounts
                # to flipping the sign of the slope
                final_m = -m

            else:
                M1 = 1 / slope_inverse
                M2 = m
                M3 = (M1 * M1 * M2 + 2 * M1 - M2) / (1 + 2 * M1 * M2 - M1 * M1)
                # print "slope", slope
                final_m = M3

            # Great, just plug in the slope and a know point on the line
            # To find the y intercept
            final_b = y0 - final_m * x0

            # print "Intercept:", x0,  y0
            # print "m:", final_m
            # print "b:", final_b

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
        return "Spherical: x = {} * y * y + {}".format(self.r, self.c)

