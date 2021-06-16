import sys, os, time
from importlib import reload
import eureka.S3_data_reduction.s3_reduce as s3
import eureka.S4_generate_lightcurves.s4_genLC as s4

eventlabel = 'wasp43b'

reload(s3)
ev3 = s3.reduceJWST(eventlabel, isplots=0, testing=False)

reload(s4)
ev4 = s4.lcJWST(ev3.eventlabel, ev3.workdir, md=ev3, isplots=0)
