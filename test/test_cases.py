# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 20:43:28 2021

@author: anant
"""

import sys
sys.path.append('/../src/')
from mapThat import mapThat
def test_answer():
    mapthat=mapThat()
    mapthat.get_api_key()
    print("Testing")
    assert mapthat.get_lat_log("2610 Cates Ave, Raleigh, NC 27606") == [35.7840099, -78.670987]
    assert mapthat.get_lat_log("1600 Pennsylvania Avenue NW, Washington, DC 20500") == [38.8976633, -77.0365739]
    assert mapthat.get_lat_log("111 S Grand Ave, Los Angeles, CA 90012") == [34.0553077, -118.2494494]
    assert mapthat.get_distance("111 S Grand Ave, Los Angeles, CA 90012",  [34.0553077, -108.2494494]) == 40722
    assert mapthat.get_distance("1600 Pennsylvania Avenue NW, Washington, DC 20500", [40.8976633, -77.0365739]) == 11758