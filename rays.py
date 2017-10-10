import numpy as np
import math
from parabolic import Parabolic
from image_plane import ImagePlane
import prescription_serializer as ps
import ray_serializer as rs


def main():
    '''
    TODO:
        - spherical surfaces
        - aspherical surfaces
        - refractive elements
            - DB of refractive indices?
            - support for different wavelengths
        - numerical cost functions
            - compare against airy disk size
        - fast optimizer
            - constants vs variables
            - constraints
        - fourier analysis?
        - graphical front end
        - 3d support
        - serialization of prescriptions and test results.  (DONE)
        - desktop mode vs cloud mode
        - aperture?
    '''
    ap = .4
    # system = [
    #     Parabolic(focal_length=-1, depth=1),
    #     Parabolic(focal_length=-1, depth=-.5),
    #     ImagePlane(depth=.5)
    # ]

    fl = .75
    system = [
        Parabolic(focal_length=-fl, depth=1),
        ImagePlane(depth=-fl)
    ]
    compile(system)

    rays = ray_fan(ap, 15, angle=2 * math.pi/180)

    ray_history = solve(system, rays)

    with open("test.rays", "w") as ofile:
        rs.dump(ray_history, ofile)
    with open("test.zemax", "w") as ofile:
        ps.dump(system, ofile)

    # for f in ray_history:
    #     print "frame"
    #     print f

def solve(system, rays):
    ray_history = []

    for element in system:
        ray_history.append(rays.copy())
        rays = element.prop(rays)

    ray_history.append(rays.copy())

    return ray_history


def compile(system):
    '''
    Things like parabolas need to know where on the X axis they reside.
    '''
    x = 0
    for element in system:
        x += element.depth
        element.set_x_offset(x)


def ray_fan(diameter, n, angle=0):
    # A line equation is defined by just y intercept and slope
    # y = mx + b

    # Angle is in radians of course
    ms = np.ones((n), dtype='float64') * math.tan(angle)
    bs = np.linspace(-diameter/2, diameter/2, n)
    xs = np.zeros((n), dtype='float64')
    ys = bs.copy()

    return np.array(zip(ms, bs, xs, ys))


def spread(summary):
    ys = summary[:, 1]
    diff = np.amax(ys) - np.amin(ys)
    print diff

if __name__ == '__main__':
    main()
