#tclean( vis='/data/moser/data_combi/DC/DC_Ly_tests//NGC346/NGC346_3by3.alma.7M.ms', 
#selectdata=True, field='NGC_346', spw='0', timerange='', uvrange='', antenna='', scan='', 
#observation='', intent='', datacolumn='corrected', 
#imagename='/data/moser/data_combi/DC/DC_Ly_tests//NGC346/NGC346.cube_INTpar_HB_PB_nIA_n2.tclean', 
#imsize=640, cell='1.4arcsec', phasecenter='ICRS 00:59:05.089680 -72.10.33.24000', stokes='I', 
#projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=7, start='230.405GHz', 
#width='3.333MHz', outframe='LSRK', veltype='radio', restfreq=['230.538GHz'], interpolation='linear', 
#gridder='mosaic', mosweight=True, pblimit=0.2, deconvolver='hogbom', scales=[0], nterms=1, smallscalebias=0.0, restoration=True, 
#restoringbeam='common', pbcor=True, outlierfile='', weighting='briggs', robust=0.5,
#niter=2, gain=0.1, threshold='0.21883350374493826Jy', interactive=0, usemask='pb', 
#mask='/data/moser/data_combi/DC/DC_Ly_tests//NGC346/NGC346.cube_INTpar_manual-tclean.mask', pbmask=0.2)






#  DC_pars_Lup3mms.py:    parameters for Lup3mms
#
#  to work with, and edit parameters here, copy this script to DC_pars.py to be used by your DC_script.py

#  inputs based on dc2019/scripts/datacomb2019_outflowsWG.py

step_title = {0: 'Concat',
              1: 'Prepare the SD-image',
              2: 'Clean for Feather/Faridani',
              3: 'Feather', 
              4: 'Faridani short spacings combination (SSC)',
              5: 'Hybrid (startmodel clean + Feather)',
              6: 'SDINT',
              7: 'TP2VIS',
              8: 'Assessment of the combination results'
              }

#thesteps=[0,1,2,3,4,5,6,8]   
#thesteps=[7]
thesteps=[0,2]

dryrun = False    # False to execute combination, True to gather filenames only

 


## Paths to the input and output files

# this script assumes the DC_locals.py has been execfiled'd - see the README.md how to do this
#  you can use _s4p_data if you want to use the configure'd setup,
#  but feel free to override
#  _s4p_data :  for read-only data
#  _s4p_work :  for reading/writing

pathtoconcat = _s4p_data + '/NGC346/'
pathtoimage  = _s4p_work + '/NGC346/'

# to quote the casaguide, "In order to run this guide you will need the following three files:"
_7ms  = 'region3by3-7M-leiden-avg.ms'
_7ms_target = 'region3by3-7M-leiden-avg_target.ms'
#_12ms = 'mst_12_nchan10_start0kms.ms'
#_sdim_fits = 'TP_12CO.fits'
_sdim = 'all.cube.spw23-forLeiden.image'

#os.system('rm -rf ' +pathtoconcat+_7ms_target)
split(vis=pathtoconcat + _7ms, outputvis=pathtoconcat + _7ms_target, 
      datacolumn='data', intent='OBSERVE_TARGET#ON_SOURCE')

# setup for concat (step 0)

a12m= [#pathtoconcat + _12ms
      ]
a7m = [pathtoconcat + _7ms_target

      ]      
weight12m = []#1.]
weight7m  = [1.]  # weigthing for REAL data !  If CASA calibration older than 4.3.0: weight: 0.193

concatms     = pathtoimage + 'NGC346_3by3.alma.7M.ms'  # path and name of concatenated file



## Files and base-names used by the combination methods (steps 1 - 8)

vis            = ''                                  # set to '' if concatms is to be used, else define your own ms-file
sdimage_input  = pathtoconcat + _sdim                #
imbase         = pathtoimage + 'NGC346'  # path + image base name
sdbase         = pathtoimage + 'NGC346'  # path + sd image base name



## Setup of the clean parameters (steps 1, 2, 5, 6, 7)

### general  - data selection and image parameters
						
t_spw         = '0' 
t_field       = 'NGC_346'
t_imsize      = 640
t_cell        = '1.4arcsec' 
t_phasecenter = 'ICRS 00:59:05.089680 -72.10.33.24000' #3 	


### spectral mode - mfs -cube
				
mode       = 'cube'          # 'mfs' or 'cube'
specsetup  =  'INTpar'       # 'SDpar' (use SD cube's spectral setup) or 'INTpar' (user defined cube setup)
                             
t_start    = '230.405GHz'    # e.g.,  0 (first chan),  '10km/s',  '10MHz'
t_width    = '3.333MHz'      # e.g.,  1 (one chan),  '-100km/s', '200GHz'
t_nchan    = 7               # e.g., -1 (all chans),        20 ,     100
t_restfreq = '230.538GHz'    # e.g., '234.567GHz'
                             			          
startchan  = None      # None  # e.g., 30, start-value of the SD image channel range you want to cut out 
endchan    = None      # None  # e.g., 39,   end-value of the SD image channel range you want to cut out
		
				      
### multiscale                

mscale     = 'HB'             # 'MS' (multiscale) or 'HB' (hogbom; MTMFS in SDINT by default!)) 
t_maxscale = -1               # for 'MS': number for largest scale size ('arcsec') expected in source


### user interaction and iterations and threshold

inter       = 'nIA'           # interactive ('IA') or non-interactive ('nIA')
nit         = 2 #000000      # number of iterations
t_cycleniter= -1              # number of minor cycle iterations before major cycle is triggered. default: -1 (CASA determined - usually sufficient), poor PSF: few 10s (low SNR) to ~ 1000 (high SNR)
t_threshold = ''              # e.g. '0.1mJy', can be left blank -> DC_run will estimate from SD-INT-AM mask for all other masking modes, too


### masking

masking  = 'PB'       # 'UM' (user mask), 'SD-INT-AM' (SD+INT+AM mask), 'AM' ('auto-multithresh') or 'PB' (primary beam)
t_mask              = pathtoimage + 'NGC346.cube_INTpar_manual-tclean.mask'      # specify for 'UM', mask name
t_pbmask            = 0.2     # specify for 'PM', cut-off level
t_sidelobethreshold = 2.0     # specify for 'AM', default: 2.0 
t_noisethreshold    = 4.25    # specify for 'AM', default: 4.25 
t_lownoisethreshold = 1.5     # specify for 'AM', default: 1.5             
t_minbeamfrac       = 0.3     # specify for 'AM', default: 0.3 
t_growiterations    = 75      # specify for 'AM', default: 75 
t_negativethreshold = 0.0     # specify for 'AM', default: 0.0 
fniteronusermask    = 0.3


#### SD-INT-AM mask fine-tuning (step 1)

theoreticalRMS = False        # use the theoretical RMS from the template image's 'sumwt', instead of measuring the RMS in a threshregion and cont_chans range of a template image
smoothing    = 5.               # smoothing of the threshold mask (by 'smoothing x beam')
threshregion = '130,324,341,522' # emission free region in template continuum or channel image
RMSfactor    = 0.5              # continuum rms level (not noise from emission-free regions but entire image)
cube_rms     = 4.               # cube noise (true noise) x this factor
cont_chans   = '0'              # line free channels for cube rms estimation
sdmasklev    = 0.3              # maximum x this factor = threshold for SD mask
				              

#### SD-INT-AM masks for all methods using tclean etc (steps 2, 5 - 7)
# options: 'SD', 'INT', 'combined'

tclean_SDAMmask = 'INT'  
hybrid_SDAMmask = 'INT'     
sdint_SDAMmask  = 'INT'     
TP2VIS_SDAMmask = 'INT' 


### SDINT options (step 6)

sdpsf   = ''
dishdia = 12.0


## SD factors for all methods (steps (3 - 7)
               
sdfac   = [1.0]               # feather parameter
SSCfac  = [1.0]               # Faridani parameter
sdfac_h = [1.0]               # Hybrid feather paramteter
sdg     = [1.0]               # SDINT parameter
TPfac   = [1.0]               # TP2VIS parameter


## TP2VIS related setup (step 7)

TPpointingTemplate        = '' #a12m[0]
listobsOutput             = imbase+'.12m.log'
TPpointinglist            = imbase+'.12m.ptg'
Epoch                     = 'ICRS'    # Epoch in listobs, e.g. 'J2000'

TPpointinglistAlternative = pathtoconcat + 'NGC346_12m.ptg'  # made from ALMA OT - make 12m covering 7m region and save pointing list -> modify formatting for TP2VIS   

TPnoiseRegion             = '47,91,104,169'  # in unregridded SD image (i.e. sdreordered = sdbase +'.SD_ro.image')
TPnoiseChannels           = '0'              # in unregridded and un-cut SD cube (i.e. sdreordered = sdbase +'.SD_ro.image')!

      
## Assessment related (step 8)

momchans = '0~6'             # line-free: '1~7,64~69'      # channels to compute moment maps (integrated intensity, etc.) 
mapchan  = 3               # cube channel (integer) of interest to use for assessment in step 8. None = central channel
				              
skymodel = ''                 # model used for simulating the observation, expected to be CASA-imported

assessment_thresh = None #0.025        # default: None, format: float, translated units: Jy/bm, threshold mask to exclude low SNR pixels, if None, use rms measurement from threshold_mask for tclean (see SD-INT-AM)

