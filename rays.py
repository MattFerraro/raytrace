import numpy as np
import math
from parabolic import Parabolic
from spherical import Spherical
from image_plane import ImagePlane
from flat import Flat
import prescription_serializer as ps
import ray_serializer as rs


def main():
    '''
    TODO:
        - serialization of prescriptions and test results.  (DONE)
        - multiple ray fan input angles (DONE)
        - start graphical front end. (DONE)
        - aperture? width of optical elements (DONE)
        - spherical surfaces

        - refractive elements
            - DB of refractive indices?
            - support for different wavelengths
        - 3d support
        - aspherical surfaces
        - elliptical surfaces?
        - numerical cost functions
            - compare against airy disk size
        - fast optimizer
            - constants vs variables
            - constraints
        - fourier analysis?
        - desktop mode vs cloud mode
    '''
    ap = .5
    fl = .75
    system = [
        Parabolic(focal_length=-2, depth=1, height=.55),
        Spherical(focal_length=-1, depth=-1, height=.35),
        Spherical(focal_length=-1, depth=2, height=.45),
        ImagePlane(depth=-1, height=ap / 2)
    ]

    compile(system)

    off_axis = 1
    num = 3
    rays_center = ray_fan(ap, num, angle=0 * math.pi/180)
    rays_down = ray_fan(ap, num, angle= -off_axis * math.pi/180)
    rays_up = ray_fan(ap, num, angle= off_axis * math.pi/180)

    all_ray_histories = []
    # all_ray_histories.append((solve(system, rays_center), "green"))
    all_ray_histories.append((solve(system, rays_down), "red"))
    all_ray_histories.append((solve(system, rays_up), "blue"))

    with open("test.rays", "w") as ofile:
        rs.dump(all_ray_histories, ofile)
    with open("test.zemax", "w") as ofile:
        ps.dump(system, ofile)

    # for hist in all_ray_histories:
    for hist in all_ray_histories:
        print "Spread:", spread(hist)


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


def ray_fan(diameter, n, angle=0, freq=550):
    # A line equation is defined by just y intercept and slope
    # y = mx + b

    # Angle is in radians of course
    ms = np.ones((n), dtype='float64') * math.tan(angle)
    bs = np.linspace(-diameter/2, diameter/2, n)
    xs = np.zeros((n), dtype='float64')
    ys = bs.copy()
    frequencies = np.array([freq] * n)

    return np.array(zip(ms, bs, xs, ys, frequencies))


def spread(history):
    frames, color = history
    last_frame = frames[-1]
    ys = last_frame[:, 3]
    diff = np.amax(ys) - np.amin(ys)
    return diff

if __name__ == '__main__':
    main()
