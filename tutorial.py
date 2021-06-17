import sys, os, time
import numpy as np
from importlib import reload
import eureka.S3_data_reduction.s3_reduce as s3
from eureka.lib import readECF as rd
from eureka.lib import logedit
from eureka.lib import readECF as rd
from eureka.lib import manageevent as me
from eureka.S3_data_reduction import optspex
from eureka.lib import astropytable
from eureka.lib import util
from eureka.S3_data_reduction import plots_s3

t0      = time.time()
eventlabel = 'wasp43b'

# Initialize metadata object
meta              = s3.Metadata()
meta.eventlabel   = eventlabel

# Initialize data object
dat              = s3.Data()

# Load Eureka! control file and store values in Event object
ecffile = 'S3_' + eventlabel + '.ecf'
ecf     = rd.read_ecf(ecffile)
rd.store_ecf(meta, ecf)

# Create directories for Stage 3 processing
datetime= time.strftime('%Y-%m-%d_%H-%M-%S')
meta.workdir = 'S3_' + datetime + '_' + meta.eventlabel
if not os.path.exists(meta.workdir):
    os.makedirs(meta.workdir)
if not os.path.exists(meta.workdir+"/figs"):
    os.makedirs(meta.workdir+"/figs")

# Load instrument module
exec('from eureka.S3_data_reduction import ' + meta.inst + ' as inst', globals())
reload(inst)

# Open new log file
meta.logname  = './'+meta.workdir + '/S3_' + meta.eventlabel + ".log"
log         = logedit.Logedit(meta.logname)
log.writelog("\nStarting Stage 3 Reduction")

# Create list of file segments
meta = util.readfiles(meta)
num_data_files = len(meta.segment_list)
log.writelog(f'\nFound {num_data_files} data file(s) ending in {meta.suffix}.fits')

stdspec = np.array([])

"""# Loop over each segment
if meta.testing_S3 == True:
    istart = num_data_files-1
else:
    istart = 0
for m in range(istart, num_data_files):
    # Report progress"""

m = 17
# Read in data frame and header
log.writelog(f'Reading file {m+1} of {num_data_files}')
dat = inst.read(meta.segment_list[m], dat, returnHdr=True)
# Get number of integrations and frame dimensions
meta.n_int, meta.ny, meta.nx = dat.data.shape
# Locate source postion
meta.src_xpos = dat.shdr['SRCXPOS']-meta.xwindow[0]
meta.src_ypos = dat.shdr['SRCYPOS']-meta.ywindow[0]
# Record integration mid-times in BJD_TDB
dat.bjdtdb = dat.int_times['int_mid_BJD_TDB']
# Trim data to subarray region of interest
dat, meta = util.trim(dat, meta)
# Create bad pixel mask (1 = good, 0 = bad)
# FINDME: Will want to use DQ array in the future to flag certain pixels
dat.submask = np.ones(dat.subdata.shape)

#Convert units (eg. for NIRCam: MJy/sr -> DN -> Electrons)
dat, meta = inst.unit_convert(dat, meta, log)

# Check if arrays have NaNs
dat.submask = util.check_nans(dat.subdata, dat.submask, log)
dat.submask = util.check_nans(dat.suberr, dat.submask, log)
dat.submask = util.check_nans(dat.subv0, dat.submask, log)

# Manually mask regions [colstart, colend, rowstart, rowend]
if hasattr(meta, 'manmask'):
    log.writelog("  Masking manually identified bad pixels")
    for i in range(len(meta.manmask)):
        ind, colstart, colend, rowstart, rowend = meta.manmask[i]
        dat.submask[rowstart:rowend,colstart:colend] = 0

# Perform outlier rejection of sky background along time axis
log.writelog('Performing background outlier rejection')
meta.bg_y1    = int(meta.src_ypos - meta.bg_hw)
meta.bg_y2    = int(meta.src_ypos + meta.bg_hw)
dat.submask = inst.flag_bg(dat, meta)


dat = util.BGsubtraction(dat, meta, log, meta.isplots_S3)


if meta.isplots_S3 >= 3:
    for n in range(meta.n_int):
        #make image+background plots
        plots_s3.image_and_background(dat, meta, n)


# Select only aperture region
ap_y1       = int(meta.src_ypos - meta.spec_hw)
ap_y2       = int(meta.src_ypos + meta.spec_hw)
dat.apdata      = dat.subdata[:,ap_y1:ap_y2]
dat.aperr       = dat.suberr [:,ap_y1:ap_y2]
dat.apmask      = dat.submask[:,ap_y1:ap_y2]
dat.apbg        = dat.subbg  [:,ap_y1:ap_y2]
dat.apv0        = dat.subv0  [:,ap_y1:ap_y2]
# Extract standard spectrum and its variance
dat.stdspec     = np.sum(dat.apdata, axis=1)
dat.stdvar      = np.sum(dat.aperr**2, axis=1)  #FINDME: stdvar >> stdspec, which is a problem
# Compute fraction of masked pixels within regular spectral extraction window
#numpixels   = 2.*meta.spec_width*subnx
#fracMaskReg = (numpixels - np.sum(apmask,axis=(2,3)))/numpixels

# Compute median frame
meta.medsubdata   = np.median(dat.subdata, axis=0)
meta.medapdata    = np.median(dat.apdata, axis=0)

# Extract optimal spectrum with uncertainties
log.writelog("  Performing optimal spectral extraction")
dat.optspec     = np.zeros((dat.stdspec.shape))
dat.opterr      = np.zeros((dat.stdspec.shape))
gain        = 1         #FINDME: need to determine correct gain
for n in range(meta.n_int):
    dat.optspec[n], dat.opterr[n], mask = optspex.optimize(dat.apdata[n], dat.apmask[n], dat.apbg[n], dat.stdspec[n], gain, dat.apv0[n], p5thresh=meta.p5thresh, p7thresh=meta.p7thresh, fittype=meta.fittype, window_len=meta.window_len, deg=meta.prof_deg, n=dat.intstart+n, isplots=meta.isplots_S3, eventdir=meta.workdir, meddata=meta.medapdata)

# Plotting results
if meta.isplots_S3 >= 3:
    for n in range(meta.n_int):
        #make optimal spectrum plot
        plots_s3.optimal_spectrum(dat, meta, n)

# Append results
if len(stdspec) == 0:
    wave_2d  = dat.subwave
    wave_1d  = dat.subwave[meta.src_ypos]
    stdspec  = dat.stdspec
    stdvar   = dat.stdvar
    optspec  = dat.optspec
    opterr   = dat.opterr
    bjdtdb   = dat.bjdtdb
else:
    stdspec  = np.append(stdspec, dat.stdspec, axis=0)
    stdvar   = np.append(stdvar, dat.stdvar, axis=0)
    optspec  = np.append(optspec, dat.optspec, axis=0)
    opterr   = np.append(opterr, dat.opterr, axis=0)
    bjdtdb   = np.append(bjdtdb, dat.bjdtdb, axis=0)

# Calculate total time
total = (time.time() - t0)/60.
log.writelog('\nTotal time (min): ' + str(np.round(total,2)))


# Save results
log.writelog('Saving results')
me.saveevent(meta, meta.workdir + '/S3_' + meta.eventlabel + "_Meta_Save", save=[])

# Save results
log.writelog('Saving results')
me.saveevent(dat, meta.workdir + '/S3_' + meta.eventlabel + "_Data_Save", save=[])

log.writelog('Saving results as astropy table...')
astropytable.savetable(meta, bjdtdb, wave_1d, stdspec, stdvar, optspec, opterr)

log.writelog('Generating figures')
if meta.isplots_S3 >= 1:
# 2D light curve without drift correction
    plots_s3.lc_nodriftcorr(meta, wave_1d, optspec)

log.closelog()



