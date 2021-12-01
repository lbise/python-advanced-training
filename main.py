#!/usr/bin/env python3
import logging
import sys
from simulator import Scenario

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    sim = logging.getLogger('simulator')
    strm = logging.StreamHandler(sys.stdout)
    frmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    strm.setFormatter(frmt)
    sim.addHandler(strm)
    sim.setLevel(logging.DEBUG)

    s = Scenario(
        incubation_duration = 15,     # Number of days before the R0 actually changes
        duration = 300,               # Days of simulation
        critical = 5000,              # Threshold for triggering lockdowns
        lockdown_duration = 60,       # Lockdown duration in days
        celebrations = [
                        74, 75, 76,   # Individual dates of celebrations
                        210, 211, 212
                       ],
        r0 = {
            "high": 2,          # R0 applied for celebrations
            "lockdown": 0.9,    # R0 applied for lockdowns
            "regular": 1.2,     # R0 applied for all other cases
        }
    )

    s.plot()
