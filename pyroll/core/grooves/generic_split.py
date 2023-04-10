import numpy as np
from numpy import tan, sin
from shapely.geometry import LineString, Polygon
from pyroll.core.grooves import GenericElongationGroove

class Split(GenericElongationGroove):
    
    def __init__(
            self,
            groove,
            depth2
    ):
        super().__init__(r1 = groove.r1, r2 = groove.r2, r3 = groove.r3, r4 = groove.r4,
                         alpha1 = groove.alpha1, alpha2 = groove.alpha2, alpha3 = groove.alpha3,
                         alpha4 = groove.alpha4, usable_width = groove.usable_width, depth = groove.depth, 
                         even_ground_width = groove.even_ground_width, indent = groove.indent)
        self.y1 = depth2
        self.z1 = self.z2.copy()

        self.y2 = 0
        #z2 is kept the same

        self.y3 = self.r1*tan(self.alpha1)*sin(self.flank_angle)
        self.z3 = self.z1 - sin(self.alpha1)

        self.y12 = self.y1 + self.r1
        self.z12 = self.z2.copy()

        self._contour_points = self._generatepoints(groove)
        self._contour_line = LineString(self._contour_points)
        self._cross_section = Polygon(self._contour_line)

        self.test_plausibility()

    def _generatepoints(self,groove):
            right_side = np.array(list(self._enumerate_contour_points()))
            left_side = np.flip(right_side, axis=0).copy()
            left_side[:, 0] *= -1
            list1 = np.concatenate([left_side, right_side[::-1]])
            list2 = groove._contour_points.copy()
            axisshift = 2*list1[-1,0]
            list1[:,0] = list1[:,0] - axisshift
            return (np.concatenate([list2,list1]))
