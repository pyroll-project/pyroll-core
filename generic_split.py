from typing import Optional
import numpy as np
from pyroll.core.grooves import GenericElongationGroove
from shapely.geometry import LineString, Polygon

class GenericSplit(GenericElongationGroove):
    """Generates a split type groove for a given generic groove"""
    
    def __init__(
            self,
            #depth, 
            groove                        
    ):
      list1 = groove._contour_points.copy()
      list2 = groove._contour_points.copy()
      rev =list1[-1,0]
      list1[:,0] = list1[:,0]-2*rev
      self._contour_points = np.concatenate([list2,list1])
      self._contour_line = LineString(self._contour_points)
      self._cross_section = Polygon(self._contour_line)
