import numpy as np


class Flat(object):
    def __init__(self, depth, height):
        self.depth = depth
        self.height = height


    def set_x_offset(self, x_offset):
        self.c = x_offset


    def prop(self, eqns):
        c = self.c

        result_ms = []
        result_bs = []
        result_xs = []
        result_ys = []
        result_freqs = []
        result_colors = []

        for eq in eqns:
            m, b, old_x, old_y, freq = eq

            x0 = c
            y0 = m * x0 + b

            # Okay we've found the intercept, let's reflect.
            # First step is to find the slope of the reflected line

            # All we gotta do is reflect off a vertical line, which amounts
            # to flipping the sign of the slope
            final_m = -m

            # Great, just plug in the slope and a known point on the line
            # To find the y intercept
            final_b = y0 - final_m * x0

            result_ms.append(final_m)
            result_bs.append(final_b)
            result_xs.append(x0)
            result_ys.append(y0)
            result_freqs.append(freq)

        return np.array(zip(
            result_ms, result_bs, result_xs, result_ys, result_freqs))


    def __str__(self):
        return "Flat: x = {} : {}".format(self.c, self.height)

