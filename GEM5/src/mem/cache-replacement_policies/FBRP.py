from m5.SimObject import SimObject
from m5.params import *

class FBRP(SimObject):
    type = 'FBRP'
    cxx_class = 'gem5::FBRP'
    cxx_header = "mem/cache/replacement_policies/fb_rp.hh"

