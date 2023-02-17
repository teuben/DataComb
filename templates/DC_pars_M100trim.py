#
#   GMC template for setting up a DC_script.py
#
#   Input are:     skymodel-c_120L.alma.cycle6.4.2018-10-02.ms
#                  (optionally more, there are 12 (8*12m + 4*7m) in this skymodel-c_120L)
#                  skymodel-c_120L.sd.image

step_title = {0: 'Concat',
              1: 'Prepare the SD-image',
              2: 'Clean for Feather/Faridani',
              3: 'Feather', 
              4: 'Faridani short spacings combination (SSC)',
              5: 'Hybrid (startmodel clean + Feather)',
              6: 'SDINT',
              7: 'TP2VIS'
              }

thesteps=[0,1,2,3,4,5,6,7]
#thesteps=[0]


#  you can use _s4p_data if you want to use the configure'd setup,
#  but feel free to override
#  _s4p_data :  for read-only data
#  _s4p_work :  for reading/writing

pathtoconcat = _s4p_data + '/skymodel-c.sim/skymodel-c_120L/'
pathtoimage  = _s4p_work + '/'



#  for optional step 0:   thevis[] -> concatms
#  otherwise concatms must contain the MS for combination

a12m=[pathtoconcat + 'skymodel-c_120L.alma.cycle6.4.2018-10-02.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.1.2018-10-02.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.4.2018-10-03.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.1.2018-10-03.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.4.2018-10-04.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.1.2018-10-04.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.4.2018-10-05.ms',
      #pathtoconcat + 'skymodel-c_120L.alma.cycle6.1.2018-10-05.ms'
      ]
      
weight12m = [1.]#, 1., 1., 1., 1., 1., 1., 1.]
        
a7m =[#pathtoconcat + 'skymodel-c_120L.aca.cycle6.2018-10-20.ms',
      #pathtoconcat + 'skymodel-c_120L.aca.cycle6.2018-10-21.ms',
      #pathtoconcat + 'skymodel-c_120L.aca.cycle6.2018-10-22.ms',
      #pathtoconcat + 'skymodel-c_120L.aca.cycle6.2018-10-23.ms'
      ]

weight7m = []#0.116, 0.116, 0.116, 0.116]  # weigthing for SIMULATED data !

##### non interactive - begin #####
thevis = a12m
thevis.extend(a7m)

#  a weight for each vis file in thevis[]

weightscale = weight12m
weightscale.extend(weight7m)

##### non interactive - end #####





#  the concatenated MS 
concatms     = pathtoimage + 'skymodel-c_120L.alma.all_int-weighted.ms'


############# input to combination methods ###########

vis             = concatms
sdimage_input   = pathtoconcat + 'skymodel-c_120L.sd.image'
imbase          = pathtoimage + 'skymodel-c_120L'            # path + image base name
sdbase          = pathtoimage + 'skymodel-c_120L'            # path + sd image base name


# TP2VIS related:
TPpointingTemplate        = a12m[0]
listobsOutput             = imbase+'.12m.log'
TPpointinglist            = imbase+'.12m.ptg'
TPpointinglistAlternative = 'user-defined.ptg' 

TPnoiseRegion             = '150,200,150,200'  # in unregridded SD image (i.e. sdreordered = sdbase +'.SD_ro.image')
TPnoiseChannels           = '2~5'              # in unregridded and un-cut SD cube (i.e. sdreordered = sdbase +'.SD_ro.image')!



mode      = 'mfs'      # 'mfs' or 'cube'
mscale    = 'HB'       # 'MS' (multiscale) or 'HB' (hogbom; MTMFS in SDINT by default!)) 
masking   = 'SD-AM'    # 'UM' (user mask), 'SD-AM' (SD+AM mask)), 'AM' ('auto-multithresh') or 'PB' (primary beam)
inter     = 'nIA'      # interactive ('IA') or non-interactive ('nIA')
nit       = 0          # max = 9.9 * 10**9 

specsetup =  'INTpar'  # 'SDpar' (use SD cube's spectral setup) or 'INTpar' (user defined cube setup)

# if "SDpar", want to use just a channel-cut-out of the SD image? , 
# else set to None (None automatically for 'INTpar'

startchan = 30  #None  # start-value of the SD image channel range you want to cut out 
endchan   = 39  #None  #   end-value of the SD image channel range you want to cut out

# resulting name part looks like
# cleansetup = '.'+ mode +'_'+ specsetup +'_'+ mscale +'_'+ masking +'_'+ inter +'_n'+ str(nit)


smoothing  = 5     # smoothing of the threshold mask (by 'smoothing x beam')
RMSfactor  = 0.5   # continuum rms level (not noise from emission-free regions but entire image)
cube_rms   = 3     # cube noise (true noise) x this factor
cont_chans = ''    # line free channels for cube rms estimation
sdmasklev  = 0.3   # maximum x this factor = threshold for SD mask



general_tclean_param = dict(#overwrite  = overwrite,
                           spw         = '0', 
                           field       = '0~68', 
                           specmode    = mode,      # ! change in variable above dict !        
                           imsize      = [1120], 
                           cell        = '0.21arcsec',    # arcsec
                           phasecenter = 'J2000 12:00:00 -35.00.00.0000',             
                           start       = 0, 
                           width       = 1, 
                           nchan       = -1, 
                           restfreq    = '',
                           threshold   = '',               # SDINT: None 
                           maxscale    = 10.,              # recommendations/explanations 
                           niter      = nit,               # ! change in variable above dict !
                           mask        = '', 
                           pbmask      = 0.4,
                           #usemask           = 'auto-multithresh',    # couple to interactive!              
                           sidelobethreshold = 2.0, 
                           noisethreshold    = 4.25, 
                           lownoisethreshold = 1.5,               
                           minbeamfrac       = 0.3, 
                           growiterations    = 75, 
                           negativethreshold = 0.0)#, 
                           #sdmasklev=0.3)   # need to overthink here 
 

sdint_tclean_param = dict(sdpsf   = '',
                         #sdgain  = 5,     # own factor! see below!
                         dishdia = 12.0)
          

sdfac   = [1.0]          # feather parameters:
SSCfac  = [1.0]          # Faridani parameters:
sdfac_h = [1.0]          # Hybrid feather paramteters:
sdg     = [1.0]          # SDINT parameters:
TPfac   = [1000000.]     # TP2VIS parameters:
          

dryrun = False    # False to execute combination, True to gather filenames only
          
          

