import numpy as np


class ImagePlane(object):
    def __init__(self, depth):
        self.depth = depth

    def set_x_offset(self, x_offset):
        self.x = x_offset

    def prop(self, eqns):
        x = self.x
        ys = []
        xs = []
        ms = []
        bs = []
        freqs = []

        # An image plane's job is to capture all the rays
        for eq in eqns:
            m, b, old_x, old_y, freq = eq
            y = m * x + b
            xs.append(x)
            ys.append(y)
            ms.append(0)
            bs.append(0)
            freqs.append(freq)

        return np.array(zip(ms, bs, xs, ys, freqs))

    def __str__(self):
        return "Image Plane: x = {}".format(self.x)
