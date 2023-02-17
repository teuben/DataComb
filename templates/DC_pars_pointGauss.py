#
#   GMC template for setting up a DC_script.py
#
#   Input are:     pointSrcGauss_3L.alma.cycle6.1.2018-10-02.ms
#                  (optionally more, there are 12 (2*12m + 1*7m) in this pointSrcGauss_3L)
#                  pointSrcGauss_3L.sd.image

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

#thesteps=[0,1,2,3,4,5,6,7,8]
thesteps=[0,1,2,3,4,5,6,8]
#thesteps=[4]

dryrun = False    # False to execute combination, True to gather filenames only
 



## Paths to the input and output files

#  you can use _s4p_data if you want to use the configure'd setup,
#  but feel free to override
#  _s4p_data :  for read-only data
#  _s4p_work :  for reading/writing

pathtoconcat = _s4p_data + '/pointSrc.sim/pointSrcGauss_3L/'
pathtoimage  = _s4p_work + '/pointGauss/'


# setup for concat (step 0)

a12m=[pathtoconcat + 'pointSrcGauss_3L.alma.cycle6.1.2018-10-02.ms',
      pathtoconcat + 'pointSrcGauss_3L.alma.cycle6.4.2018-10-02.ms'
      ]
a7m =[pathtoconcat + 'pointSrcGauss_3L.aca.cycle6.2018-10-05.ms'
      ]         
weight12m = [1., 1.]
weight7m = [0.116]  # weigthing for SIMULATED data !

concatms     = pathtoimage + 'pointGauss.alma.all_int-weighted.ms'       # path and name of concatenated file



## Files and base-names used by the combination methods (steps 1 - 8)

vis            = ''                                    # set to '' if concatms is to be used, else define your own ms-file
sdimage_input  = pathtoconcat + 'pointSrcGauss_3L.sd.image'
imbase         = pathtoimage + 'pointGauss'            # path + image base name
sdbase         = pathtoimage + 'pointGauss'            # path + sd image base name



## Setup of the clean parameters (steps 1, 2, 5, 6, 7)

### general  - data selection and image parameters

t_spw         = '0' 
t_field       = '0~68' 
t_imsize      = [1120] 
t_cell        = '0.21arcsec'  # add 'arcsec' to value
t_phasecenter = 'J2000 12:00:00 -35.00.00.0000'  # pointing / mosaic center


### spectral mode - mfs -cube

mode       = 'mfs'            # 'mfs' or 'cube'
specsetup  = 'INTpar'         # 'SDpar' (use SD cube's spectral setup) or 'INTpar' (user defined cube setup)
					          
t_start    = 0                # e.g.,  0 (first chan),  '10km/s',  '10MHz'
t_width    = 1                # e.g.,  1 (one chan),  '-100km/s', '200GHz'
t_nchan    = -1               # e.g., -1 (all chans),        20 ,     100
t_restfreq = ''               # e.g., '234.567GHz'
                 			          
startchan  = 30               # None, or e.g., 30, start-value of the SD image channel range you want to cut out 
endchan    = 39               # None, or e.g., 39,   end-value of the SD image channel range you want to cut out


### multiscale                
	
mscale     = 'MS'             # 'MS' (multiscale) or 'HB' (hogbom; MTMFS in SDINT by default!)) 
t_maxscale = -1               # for 'MS': number for largest scale size ('arcsec') expected in source


### user interaction and iterations and threshold

inter       = 'nIA'           # interactive ('IA') or non-interactive ('nIA')
nit         = 10000000        # number of iterations
t_cycleniter= -1              # number of minor cycle iterations before major cycle is triggered. default: -1 (CASA determined - usually sufficient), poor PSF: few 10s (low SNR) to ~ 1000 (high SNR)
#t_threshold = '0.005Jy'       # = 7*5*RMS in box from step 1 - but make mask at another level i.e. RMSfactor 1500 
#t_threshold = '0.05Jy'       # 1/4 level of residual ring in sdint for mask smooth 20
t_threshold = '0.02Jy'       # 1/4 level of residual ring in sdint for mask smooth 20

### masking

masking             = 'SD-INT-AM'    # 'UM' (user mask), 'SD-INT-AM' (SD+INT+AM mask), 'AM' ('auto-multithresh') or 'PB' (primary beam)
t_mask              = ''      # specify for 'UM', mask name
t_pbmask            = 0.2     # specify for 'PM', cut-off level
t_sidelobethreshold = 2.0     # specify for 'AM', default: 2.0 
t_noisethreshold    = 4.25    # specify for 'AM', default: 4.25 
t_lownoisethreshold = 1.5     # specify for 'AM', default: 1.5             
t_minbeamfrac       = 0.3     # specify for 'AM', default: 0.3 
t_growiterations    = 75      # specify for 'AM', default: 75 
t_negativethreshold = 0.0     # specify for 'AM', default: 0.0 
fniteronusermask    = 1.0 


#### SD-INT-AM mask fine-tuning (step 1)

theoreticalRMS = False        # use the theoretical RMS from the template image's 'sumwt', instead of measuring the RMS in a threshregion and cont_chans range of a template image
smoothing    = 20. #15.  25.=> clean diverges              # smoothing of the threshold mask (by 'smoothing x beam')
threshregion = '924,48,1111,169' # emission free region in template continuum or channel image
RMSfactor    = 1500.0            # continuum rms level (not noise from emission-free regions but entire image)
cube_rms     = 3.                # cube noise (true noise) x this factor
cont_chans   = ''                # line free channels for cube rms estimation
sdmasklev    = 0.3               # maximum x this factor = threshold for SD mask
	

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

TPpointingTemplate        = a12m[0]
listobsOutput             = imbase+'.12m.log'
TPpointinglist            = imbase+'.12m.ptg'
Epoch                     = 'J2000'    # Epoch in listobs, e.g. 'J2000'

TPpointinglistAlternative = 'user-defined.ptg' 

TPnoiseRegion             = '41,41,100,100'  # in unregridded SD image (i.e. sdreordered = sdbase +'.SD_ro.image')
TPnoiseChannels           = '2~5'            # in unregridded and un-cut SD cube (i.e. sdreordered = sdbase +'.SD_ro.image')!

  
## Assessment related (step 8)
          
momchans = ''                 # channels to compute moment maps (integrated intensity, etc.) 
mapchan = None                # cube channel (integer) of interest to use for assessment in step 8

skymodel=a12m[0].replace('.ms','.skymodel')    # model used for simulating the observation, expected to be CASA-imported

assessment_thresh = 0.01        # default: None, option: None, 'clean-thresh', or flux value(float, translated units: Jy/bm), 
                                       # threshold mask to exclude low SNR pixels, if None, use rms measurement from threshold_mask for tclean (see SD-INT-AM)
                                       # also used as lower flux limit for moment 0 map creation

