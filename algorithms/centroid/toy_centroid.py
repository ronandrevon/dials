# toy centroid implementation: this is deliberately bad to illustrate how the
# interface works and how things could be improved

from dials.interfaces.centroid.centroid_interface_prototype import \
    centroid_interface_prototype as centroid_interface

class toy_centroid(centroid_interface):
    def __init__(self, bounding_boxes, dxtbx_sweep_object):
        centroid_interfaces.__init__(self, bounding_boxes, dxtbx_sweep_object)

        self._image_size = self._sweep.get_detector().get_size()

        return

    def compute_centroid_from_bbox(self, bbox):

        import math

        fmin, fmax, rmin, rmax, cmin, cmax = bbox

        # build the list of pixels - let's be dumb and just have a literal
        # list

        pixel_list = []

        for f in range(f_min, f_max):
            data = self._sweep[f]
            for r in range(r_min, r_max):
                for c in range(c_min, c_max):
                    pixel_list.append(
                        (f, r, c, data[r * self._image_size[0] + c]))

        # compute averages of positions

        f_tot = 0.0
        r_tot = 0.0
        c_tot = 0.0
        d_tot = 0.0

        for f, r, c, d in pixel_list:
            f_tot += d * f
            r_tot += d * r
            c_tot += d * c
            d_tot += d

        assert(d_tot)

        _f, _r, _c = f_tot / d_tot, r_tot / d_tot, c_tot / d_tot

        # now compute the variance

        f_tot = 0.0
        r_tot = 0.0
        c_tot = 0.0
        d_tot = 0.0

        for f, r, c, d in pixel_list:
            f_tot += d * (f - _f) ** 2
            r_tot += d * (r - _r) ** 2
            c_tot += d * (c - _c) ** 2
            d_tot += d

        _sf = math.sqrt(f_tot / d_tot)
        _sr = math.sqrt(r_tot / d_tot)
        _sc = math.sqrt(c_tot / d_tot)

        return _f, _r, _c, _sf, _sr, _sc
