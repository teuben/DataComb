# do not modify the parameters in this script, instead use DC_pars.py
# See DC_script.py for an example how to use this script,
# users typically do not run this script directly

# After DC_pars.py defines the parameters this script works in two steps:
#   - set up the filenames for a convention we use in the DC project
#   - provide a number of snippets of code (currently 8) that can all
#     or individually be selected to run. It uses routines from
#     datacomb.py and standard CASA6 routines.


step_title = {0: 'Concat (optional)',
              1: 'Prepare the SD-image',
              2: 'Clean for Feather/Faridani',
              3: 'Feather', 
              4: 'Faridani short spacings combination (SSC)',
              5: 'Hybrid (startmodel clean + Feather)',
              6: 'SDINT',
              7: 'TP2VIS',
              8: 'Assessment'
              }


import os 
import sys 
import numpy as np  
import casatasks as cta

from importlib import reload  
import datacomb as dc
import IQA_script as iqa
# we do a reload here, because we often edit these in the same casa session
reload(dc)
reload(iqa)


import time
start = time.time()

decimal_places=6


### Tidy up old left-overs from previous runs 
# switch this off, if you run multiple casa instances/DC_runs in the 
# same work folder !  Else you delete files from another working process
#          
#os.system('rm -rf '+pathtoimage + 'TempLattice*')


### user information

print(' ')
print('### ')
if dryrun==True:
    print('Collecting filenames for assessment of ...')   
else:     
    print('Will be executing the following steps ...')    
for mystep in thesteps:
    print('step ', mystep, step_title[mystep])
    
print('### ')
print(' ')



print(' ')
print('### ')
version = dc.get_casa_version()
print('You are running CASA version', version, '.')
if (2 in thesteps) or (5 in thesteps) or (6 in thesteps) or (7 in thesteps):
    if version < '6.2.0':
        print('All cleans are done with briggs weighting.')
    if version >= '6.2.0':
        print('All cubes are cleaned with briggsbwtaper weighting, except from sdintimaging (step 6, briggs weighting).')
        print('All mfs images are cleaned with briggs weighting.')
        print('sdintimaging does not offer mfs-mode in CASA >= 6.2.0')
#print('### ')
print('### ')
print(' ')




### put together file names and weights for concat, we allow 12m or 7m to be absent
thevis = []
weightscale = []

for i in range(len(a12m)):
    if weight12m[i] > 0:
        print("CONCAT will be using",a12m[i])
        thevis.append(a12m[i])
        weightscale.append(weight12m[i])
for i in range(len(a7m)):
    if weight7m[i] > 0:
        print("CONCAT will be using",a7m[i])
        thevis.append(a7m[i])
        weightscale.append(weight7m[i])


### define ms-file to perform combination on and file check 
if vis=='':
    vis = concatms
    if not os.path.exists(vis):
        if dryrun==True:
            pass 
        elif 0 in thesteps:
            pass
        else:    
            thesteps.append(0)      
            thesteps.sort()           # force execution of vis creation (Step 0)
            print('Need to execute step 0 to generate a concatenated ms')
else:
    dc.file_check(vis)  
    os.system('rm -rf '+vis+'.listobs')
    cta.listobs(vis, listfile=vis+'.listobs')  



### set up tclean parameter dictionary 
general_tclean_param = dict(#overwrite  = overwrite,
                           specmode    = mode,             
                           niter       = nit,     
                           cycleniter  = t_cycleniter,       
                           spw         = t_spw,  
                           field       = t_field, 
                           imsize      = t_imsize,     
                           cell        = t_cell,         
                           phasecenter = t_phasecenter,  
                           start       = t_start,      
                           width       = t_width,      
                           nchan       = t_nchan,      
                           restfreq    = t_restfreq,   
                           threshold   = t_threshold,    
                           maxscale    = t_maxscale,     
                           mask        = t_mask,       
                           pbmask      = t_pbmask,
                           sidelobethreshold = t_sidelobethreshold, 
                           noisethreshold    = t_noisethreshold, 
                           lownoisethreshold = t_lownoisethreshold,               
                           minbeamfrac       = t_minbeamfrac, 
                           growiterations    = t_growiterations,    
                           negativethreshold = t_negativethreshold)

### additional sdintimaging-specific parameters 
sdint_tclean_param = dict(sdpsf   = sdpsf,
                          dishdia = dishdia)
          


### naming scheme specific inputs:

if mode == 'mfs':
    specsetup =  'nt1'                            # number of Taylor terms (compare mtmfs)

if inter == 'IA':
    general_tclean_param['interactive'] = 1       # use 1 instead of True to get tclean feedback dictionary !
elif inter == 'nIA':
    general_tclean_param['interactive'] = 0       # use 0 instead of False to get tclean feedback dictionary !  
 
if mscale == 'HB':
    general_tclean_param['multiscale'] = False
if mscale == 'MS':
    general_tclean_param['multiscale'] = True     # automated scale choice dependant on maxscale




############## naming convention ############

###### NONIT seems to be not needed anymore ####
cleansetup_nonit = '.'+ mode +'_'+ specsetup +'_'+ mscale +'_'+ masking +'_'+ inter
cleansetup = cleansetup_nonit +'_n'+ str(nit)


### output of combination methods ('combisetup')

tcleansetup  = '.tclean'
feathersetup = '.feather_f'  # added during combination: + str(sdfac)
SSCsetup     = '.SSC_f'      # added during combination: + str(SSCfac)
hybridsetup  = '.hybrid_f'   # added during combination: + str(sdfac_h)
sdintsetup   = '.sdint_g'    # added during combination: + str(sdg)
TP2VISsetup  = '.TP2VIS_t'   # added during combination: + str(TPfac)






##### intermediate products name for step 1 = gather information - no need to change!

# SD image axis-reordering, cut-out and regridding, mask names 

sdreordered = sdbase +'.SD_ro.image'                        # SD image axis-reordering

if startchan!= None and endchan!=None and specsetup == 'SDpar':
    sdbase = sdbase + '_ch'+str(startchan)+'-'+str(endchan)
else:
    pass 
    
sdreordered_cut = sdbase +'.SD_ro.image'                    # SD image axis-reordering
sdroregrid      = sdbase +'.SD_ro-rg_'+specsetup+'.image'   # SD image regridding

imnameth        = imbase + '.'+mode +'_'+ specsetup +'_template'  # dirty image for thershold and mask generation
threshmask      = imbase + '.'+mode +'_'+ specsetup+ '_RMS'       # thresold mask name
SD_mask_root    = sdbase + '.'+mode +'_'+ specsetup+ '_SD'        # SD mask name
combined_mask   = SD_mask_root + '-RMS.mask'                      # SD+AM+threshold mask name



# masking mode setup

if masking == 'PB':
    general_tclean_param['usemask'] = 'pb'
if masking == 'AM':
    general_tclean_param['usemask'] = 'auto-multithresh'                   
if masking == 'UM':
    #general_tclean_param['usemask'] = 'user'
    general_tclean_param['usemask']     = 'auto-multithresh'   
    general_tclean_param['loadmask']    = True   
    general_tclean_param['fniteronusermask']  = fniteronusermask  
if masking == 'SD-INT-AM': 
    if not os.path.exists(combined_mask) or not os.path.exists(threshmask+'.mask') or not os.path.exists(SD_mask_root+'.mask'):
        if 1 in thesteps:
            pass
        else:    
            thesteps.append(1)      
            thesteps.sort()           # force execution of SDint mask creation (Step 1)
            print('Need to execute step 1 to generate an image mask')
    general_tclean_param['usemask']     = 'auto-multithresh'   
    general_tclean_param['loadmask']    = True   
    general_tclean_param['fniteronusermask']  = fniteronusermask   
    




# translate SD-INT-AM masks per combination method

SDAMmasks_userinput = [tclean_SDAMmask, hybrid_SDAMmask, sdint_SDAMmask, TP2VIS_SDAMmask]

for i in range(0,len(SDAMmasks_userinput)):
    if SDAMmasks_userinput[i]=='INT':
        SDAMmasks_userinput[i]=threshmask+'.mask'
    elif SDAMmasks_userinput[i]=='SD':
        SDAMmasks_userinput[i]=SD_mask_root+'.mask'
    elif SDAMmasks_userinput[i]=='combined':
        SDAMmasks_userinput[i]=combined_mask
    else:
        sys.exit()

tclean_mask, hybrid_mask, sdint_mask, TP2VIS_mask = SDAMmasks_userinput


# specsetup 

if specsetup == 'SDpar':
    if not os.path.exists(sdreordered_cut):
        if 1 in thesteps:
            pass
        else:    
            thesteps.append(1)      
            thesteps.sort()           # force execution of SDint mask creation (Step 1)
            print('Need to execute step 1 to reorder image axes of the SD image')
    elif os.path.exists(sdreordered_cut):
        # read SD image frequency setup as input for tclean    
        cube_dict = dc.get_SD_cube_params(sdcube = sdreordered_cut) #out: {'nchan':nchan, 'start':start, 'width':width}
        general_tclean_param['start'] = cube_dict['start']  
        general_tclean_param['width'] = cube_dict['width']
        general_tclean_param['nchan'] = cube_dict['nchan']
        sdimage = sdreordered_cut  # for SD cube params used
elif specsetup == 'INTpar' or specsetup == 'nt1':
    if not os.path.exists(sdroregrid):
        if 1 in thesteps:
            pass
        else:    
            thesteps.append(1)      
            thesteps.sort()           # force execution of SDint mask creation (Step 1)
            print('Need to execute step 1 to regrid SD image')
    elif os.path.exists(sdroregrid):
        sdimage = sdroregrid  # for INT cube params used




# mask-generation: common tclean parameters needed for creating a simple dirty image in step 1

rederivethresh=True   # TP2VIS parameter to derive threshold for SD+INT.ms  

mask_tclean_param = dict(phasecenter = general_tclean_param['phasecenter'],
                         spw =      general_tclean_param['spw'], 
                         field =    general_tclean_param['field'], 
                         imsize =   general_tclean_param['imsize'], 
                         cell =     general_tclean_param['cell'],
                         specmode = general_tclean_param['specmode'],
                         start =    general_tclean_param['start'],
                         width =    general_tclean_param['width'],
                         nchan =    general_tclean_param['nchan'],
                         restfreq = general_tclean_param['restfreq']
                         )


# mask generation: execute step 1 or 2, or use existing template 
tcleanname = imbase + cleansetup + tcleansetup   

if 1 in thesteps and dryrun==False: 
        pass    
elif not os.path.exists(imnameth + '.image'): # or not os.path.exists(tcleanname + '.image'):
#elif not os.path.exists(threshmask + '.mask') or not os.path.exists(imnameth + '.image'):
    #if 1 in thesteps:
    #    pass
    #else:    
    thesteps.append(1)      
    thesteps.sort()           # force execution of SDint mask creation (Step 1)
    print('Need to execute step 1 to estimate a thresold')
else: #if imnameth/tcleanname + '.image' exists, simply re-derive the mask etc.
    if os.path.exists(tcleanname + '.image'):
        tempname = tcleanname
        print('')
        print('Derive mask and threshold from tcleaned image (step 2).')
    else:
        tempname = imnameth
        print('')
        print('Derive mask and threshold from dirty image (step 1).')

    #thresh = dc.derive_threshold(#vis, 
    #                             imnameth , threshmask,
    #                             #overwrite=False,   # False for read-only, 
    #                             specmode = general_tclean_param['specmode'],
    #                             smoothing = smoothing,
    #                             threshregion = threshregion,
    #                             RMSfactor = RMSfactor,
    #                             cube_rms   = cube_rms,    
    #                             cont_chans = cont_chans,
    #                             #**mask_tclean_param
    #                             makemask=True)
    #    
        
    thresh = dc.make_masks_and_thresh(tempname, threshmask,
                                         #overwrite=True,
                                 sdimage, sdmasklev, SD_mask_root,
                                 combined_mask,                                         
                                 specmode = general_tclean_param['specmode'],
                                 smoothing = smoothing,
                                 threshregion = threshregion,
                                 RMSfactor = RMSfactor,
                                 cube_rms   = cube_rms,    
                                 cont_chans = cont_chans,
                                 theoreticalRMS=theoreticalRMS,
                                 makemask=True
                                 )        

    print(' ')   
                    
    if general_tclean_param['threshold'] == '':                         # don't forget to run *_pars_* before
        rederivethresh=True  # TP2VIS parameter 
        general_tclean_param['threshold']  = str(thresh)+'Jy' 
        #print('### Use mask threshold as clean threshold ', general_tclean_param['threshold']) 
        print('### Use INT mask threshold as clean threshold ', round(thresh, decimal_places), 'Jy' )          
    else:
        rederivethresh=False  # TP2VIS parameter 
        print('### Use user-defined clean threshold ', general_tclean_param['threshold'])          
            











####### collect file names for assessment ######

tcleanims  = []
featherims = []
SSCims     = []
hybridims  = []
sdintims   = []
TP2VISims  = []


# step numbers for filename suffix 
thesteps2 = map(str, thesteps)    
stepsjoin=''.join(thesteps2)
steps=stepsjoin.replace('0','').replace('1','').replace('8','')
steplist='_s'+steps       # for assessment (step 8)
steplist2='_s'+stepsjoin  # for runtime measurement 




    
mystep = 0    ###################----- CONCAT -----####################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')    
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])

    print('### ------------------------------------------------')
    print(' ')





    if dryrun == True:
        print('Skip execution!')
    else:   
        if thevis ==[]:
            print('No data to concat!')
            
        else: 
            print('  vis:')
            print(*thevis, sep = "\n")
            print('  concatvis:')
            print(concatms)  
            
            for i in range(0,len(thevis)):
                if '.aca.tp.' in thevis[i]:
                    print('')
                    print('')
                    print('-------------------------------- ! ERROR ! --------------------------------')
                    print('')
                    print(thevis[i]+' is a total power/single dish data set.')
                    print('Cannot concatenate it into an interferometric data set.')
                    print('')
                    print('-------------------- ! ABORT PROGRAM WITH SYSTEMEXIT ! --------------------')
                    print('')
                    print('')
                    sys.exit()       
                else:               
                    dc.check_CASAcal(thevis[i])    
            
            print(' ')         
            print('Starting CONCAT')         

            os.system('rm -rf '+concatms)
            
            cta.concat(vis = thevis, concatvis = concatms, visweightscale = weightscale)

            os.system('rm -rf '+concatms+'.listobs')
            cta.listobs(concatms, listfile=concatms+'.listobs')

            print('--- Done! ---')         





mystep = 1    #########----- PREPARE SD-IMAGE and MASKS -----##########
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')    
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')

    if dryrun == True:
        print('Skip execution!')
    else:    

        # axis reordering       
        print(' ')         
        print('--- Reorder SD image axes ---')                          
        dc.reorder_axes(sdimage_input, sdreordered)
        print('--- Axis reorder done! --- ')         
       
       
        
        # make a channel-cut-out from the SD image?
        if sdreordered!=sdreordered_cut:
            print(' ')         
            print('--- Make a channel-cut-out from the SD image from channel', startchan, 'to', endchan, '--- ')  
            dc.channel_cutout(sdreordered, sdreordered_cut, startchan = startchan,
                              endchan = endchan)
            print('--- Channel-cut-out done! --- ')         


        
        # read SD image frequency setup as input for tclean    
        if specsetup == 'SDpar':
            print(' ')         
            print('--- Read SD image frequency setup as input for tclean ---')              
            cube_dict = dc.get_SD_cube_params(sdcube = sdreordered_cut) #out: {'nchan':nchan, 'start':start, 'width':width}
            general_tclean_param['start'] = cube_dict['start']  
            general_tclean_param['width'] = cube_dict['width']
            general_tclean_param['nchan'] = cube_dict['nchan']
            sdimage = sdreordered_cut  # for SD cube params used   
            print('--- Tclean frequency setup done! --- ')         

        
        
        # make dirty image 
        print(' ')         
        print('--- Make dirty image for regridding SD image and INT mask --- ')                                  

        dc.runtclean(vis,imnameth,
                     niter=0, interactive=False,
                     **mask_tclean_param)


        # regrid SD image frequency axis to tclean (requires runtclean to be run)    
        if specsetup == 'SDpar':
            sdimage = sdreordered_cut  # for SD cube params used
        else:
            print('')
            print('--- Regrid SD image --- ')
            os.system('rm -rf '+sdroregrid)
            dc.regrid_SD(sdreordered_cut, sdroregrid, imnameth+'.image')
            sdimage = sdroregrid  # for INT cube params used
            print('--- Regridding done! --- ')     
            ## just for testing - if it fails then the common beam in regridSD didn't work 
            #hdr = imhead(sdimage,mode='summary')
            #beam_major = hdr['restoringbeam']['major']    
     



        # Derive INT threshold, INT mask, SD mask, and combined mask

        thresh = dc.make_masks_and_thresh(imnameth, threshmask,
                                     #overwrite=True,
                                     sdimage, sdmasklev, SD_mask_root,
                                     combined_mask,
                                     specmode = general_tclean_param['specmode'],
                                     smoothing = smoothing,
                                     threshregion = threshregion,
                                     RMSfactor = RMSfactor,
                                     cube_rms   = cube_rms,    
                                     cont_chans = cont_chans,
                                     theoreticalRMS=theoreticalRMS,
                                     makemask=True
                                     )
                                      

  

        print(' ')   
     
        if general_tclean_param['threshold'] == '':
            rederivethresh=True  # TP2VIS parameter 
            #userthresh=False    ### parameter gone?
            general_tclean_param['threshold']  = str(thresh)+'Jy' 
            print('### Use INT mask threshold as clean threshold ', round(thresh, decimal_places), 'Jy' )          
            #print('Set the tclean-threshold to ', general_tclean_param['threshold'])
        else:
            rederivethresh=False  # TP2VIS parameter 
            #userthresh=True     ### parameter gone?
            print('### Use user-defined clean threshold ', general_tclean_param['threshold'])          
           
       
           

mystep = 2    ############----- CLEAN FOR FEATHER/SSC -----############
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')
    

    imname = imbase + cleansetup + tcleansetup
       
    if masking == 'SD-INT-AM': 
        general_tclean_param['mask']  = tclean_mask

    z = general_tclean_param.copy()   

    if dryrun == True:
        print('Skip execution!')        
    else:
        dc.runtclean(vis, imname, startmodel='', 
                     **z)

    
        # update masking for tcleaned image as template !

        # Derive INT threshold, INT mask, SD mask, and combined mask

        thresh = dc.make_masks_and_thresh(imname, threshmask,
                                     #overwrite=True,
                                     sdimage, sdmasklev, SD_mask_root,
                                     combined_mask,
                                     specmode = general_tclean_param['specmode'],
                                     smoothing = smoothing,
                                     threshregion = threshregion,
                                     RMSfactor = RMSfactor,
                                     cube_rms   = cube_rms,    
                                     cont_chans = cont_chans,
                                     theoreticalRMS=theoreticalRMS,
                                     makemask=True
                                     )

        print(' ')   
     
        if general_tclean_param['threshold'] == '':
            rederivethresh=True  # TP2VIS parameter 
            #userthresh=False    ### parameter gone?
            general_tclean_param['threshold']  = str(thresh)+'Jy' 
            print('### Use INT mask threshold as clean threshold ', round(thresh, decimal_places), 'Jy' )          
            #print('Set the tclean-threshold to ', general_tclean_param['threshold'])
        else:
            rederivethresh=False  # TP2VIS parameter 
            #userthresh=True     ### parameter gone?
            print('### Use user-defined clean threshold ', general_tclean_param['threshold'])          
           



    tcleanims.append(imname+'.image')





mystep = 3    ###################----- FEATHER -----###################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')

    #intimage='/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.image_ro_reg'
    #intpb='/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.pb_ro_reg'
    intimage = imbase + cleansetup + tcleansetup + '.image'
    intpb    = imbase + cleansetup + tcleansetup + '.pb'
    
    for i in range(0,len(sdfac)):
        
        #imname = '/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L' + feathersetup + str(sdfac[i]) 
        imname = imbase + cleansetup + feathersetup + str(sdfac[i]) 
                    
        if dryrun == True:
            print('Skip execution!')
        else:
            dc.runfeather(intimage, intpb, sdimage, sdfactor = sdfac[i],
                          featherim = imname)


        featherims.append(imname+'.image')





mystep = 4    ################----- FARIDANI SSC -----#################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')


    #intimage='/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.image_ro_reg'
    #intpb='/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.pb_ro_reg'
    intimage = imbase + cleansetup + tcleansetup + '.image'
    intpb    = imbase + cleansetup + tcleansetup + '.pb'

    for i in range(0,len(SSCfac)):
        #imname = '/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L'  + SSCsetup + str(SSCfac[i]) 
        imname = imbase + cleansetup + SSCsetup + str(SSCfac[i]) 
        
        if dryrun == True:
            print('Skip execution!')
        else:
            os.system('rm -rf '+imname+'*')

            dc.ssc(highres=intimage, lowres=sdimage, pb=intpb,
                   sdfactor = SSCfac[i], combined=imname) 
   
                   
        SSCims.append(imname+'.image')





mystep = 5    ###################----- HYBRID -----####################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')


    if masking == 'SD-INT-AM': 
        general_tclean_param['mask']  = hybrid_mask

    z = general_tclean_param.copy()   

    for i in range(0,len(sdfac_h)):
        imname = imbase + cleansetup + hybridsetup 
        
        if dryrun == True:
            print('Skip execution!')
        else:                       
            dc.runWSM(vis, sdimage, imname, sdfactorh = sdfac_h[i],
                      **z)

                                
        hybridims.append(imname+str(sdfac_h[i])+'.image')



mystep = 6    ####################----- SDINT -----####################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')
    
    
    if masking == 'SD-INT-AM': 
        general_tclean_param['mask']  = sdint_mask

    z = general_tclean_param.copy()   
    z.update(sdint_tclean_param)
    
    for i in range(0,len(sdg)) :
        jointname = imbase + cleansetup + sdintsetup + str(sdg[i]) 
        
        if dryrun == True:
            print('Skip execution!')
        else:
            dc.runsdintimg(vis, sdimage, jointname, sdgain = sdg[0],
                           **z)


        sdintims.append(jointname+'.image')                
     
     
     
                
                
mystep = 7    ###################----- TP2VIS -----####################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')


    # get 12m pointings to simulate TP observation as interferometric
     
    if dryrun == True:
        print('Skip execution!')
    else:    
        if TPpointingTemplate!='' and dc.file_check_vis_str_only(TPpointingTemplate)==TPpointingTemplate: #a12m!=[]:    # if 12m-data exists ...
            print('Creating pointing table from template data set:', TPpointingTemplate)
            #dc.ms_ptg(TPpointingTemplate, outfile=TPpointinglist, uniq=True)
            dc.listobs_ptg(TPpointingTemplate, listobsOutput, TPpointinglist, Epoch=Epoch)
        else:
            print('Using user-provided pointing table:', TPpointinglistAlternative)
            TPpointinglist = TPpointinglistAlternative    
        print('')
    
    # create 'TP.ms', i.e. SD visibilities  
    
    if specsetup == 'SDpar':
        imTP = sdreordered_cut
    else:
        imTP = sdreordered
    TPresult= imTP.replace('.image','.ms')
    imname1 = imbase + cleansetup + TP2VISsetup  # first plot
     
    if dryrun == True:
        pass
    else:    
        dc.create_TP2VIS_ms(imTP=imTP, TPresult=TPresult,
            TPpointinglist=TPpointinglist, mode=mode,  
            vis=vis, imname=imname1, TPnoiseRegion=TPnoiseRegion, 
            TPnoiseChannels=TPnoiseChannels)  


    # bring TP.ms and INT.ms on same spectral reference frame before tclean
    #
    # models typically do not need this, so we have a new (but optional)
    # no_transform = True variable in DC_pars.py
    
    transvis = vis+'_LSRK' 

    if dryrun == True:
        pass
    else:
        if not 'no_transform' in locals():
            no_transform = False
        if not no_transform:
            dc.transform_INT_to_SD_freq_spec(TPresult, imTP, vis, 
                                             transvis, datacolumn='DATA', outframe='LSRK')
        else:
            transvis = vis

    # make TP2VIS image (tclean)
    
    if masking == 'SD-INT-AM': 
        general_tclean_param['mask']  = TP2VIS_mask

    z = general_tclean_param.copy()   
    z['rederivethresh']=rederivethresh
   
    for i in range(0,len(TPfac)) :
        imname = imbase + cleansetup + TP2VISsetup + str(TPfac[i])
        
        vis=transvis #!
        
        if dryrun == True:
            pass
        else:
            dc.runtclean_TP2VIS_INT(TPresult, TPfac[i], vis, imname,
                                    RMSfactor=RMSfactor, threshregion=threshregion,
                                    cube_rms=cube_rms, cont_chans = cont_chans, 
                                    theoreticalRMS=theoreticalRMS, **z)   

        if os.path.exists(imname+'.tweak.image'):
            TP2VISims.append(imname+'.tweak.image')
        else:
            TP2VISims.append(imname+'.image')
        




mystep = 8    #################----- ASSESSMENT -----##################
if mystep in thesteps:
    cta.casalog.post('### ','INFO')
    cta.casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    cta.casalog.post('### ','INFO')
    print(' ')
    print('### ------------------------------------------------')
    print('Step ', mystep, step_title[mystep])
    print('### ------------------------------------------------')
    print(' ')


    # set assessment threshold value

    if assessment_thresh == None:   
        if mode=='cube':
            image_rms = thresh/cube_rms #*3.     # 3 sigma limit
        if mode=='mfs':
            image_rms = thresh/RMSfactor #*3.    # 3 sigma limit
        clip_string = 'Clipping maps at rms level of '+str(round(image_rms,decimal_places))+ ' Jy/beam'                                             
    elif assessment_thresh == 'clean-thresh':
        image_rms = float(general_tclean_param['threshold'].replace('Jy',''))
        clip_string = 'Clipping maps at clean threshold level of '+str(round(image_rms,decimal_places))+ ' Jy/beam' 
    else:
        image_rms = assessment_thresh
        clip_string = 'Clipping maps at user-defined level of '+str(round(image_rms,decimal_places))+ ' Jy/beam'

    

    print('###')    
    print('### Assessment: '+clip_string)       
    #print('### Clipping level for the assessment of the maps was at %.6f Jy/beam' %image_rms)       
    print('###') 
    print('') 

    
    #### imbase         = pathtoimage + 'skymodel-b_120L
    sourcename = imbase.replace(pathtoimage,'')
    # folder to put the assessment images to 
    assessment=pathtoimage + 'assessment_'+sourcename+cleansetup+'_thresh'+str(round(image_rms,6))
    os.system('mkdir '+assessment) 


    ########## list residuals, threshold and stopping criteria ############
    
    tcleanres = []
    hybridres = []
    sdintres  = []
    TP2VISres = []
    
    if (2 in thesteps) or (3 in thesteps) or (4 in thesteps): # and (tcleanres != []): 
        tcleanres = [imbase + cleansetup + tcleansetup + '.image']
    if 5 in thesteps: hybridres = [imbase + cleansetup + hybridsetup + '.image']
    if 6 in thesteps: sdintres  = sdintims                                    
    if 7 in thesteps: TP2VISres = TP2VISims                                   
    
    allcombires=tcleanres + hybridres + sdintres + TP2VISres
    
    allcombires = [a.replace('.tweak','') for a in allcombires]
    allcombires = [a.replace('.image','.residual') for a in allcombires]
    allcombimask = [a.replace('.residual','.mask') for a in allcombires]
    allcombitxt = [a.replace('.residual', '') for a in allcombires]
    #print(allcombimask)
    #print(allcombires[0])
    
    stop_crit=[]
    cleanthresh=[]
    cleaniterdone = []
    
    if mapchan==None:
        mapchan=int(general_tclean_param['nchan']/2.)
    
    if nit>0:
        
        print(' ')
        print(' ')
        print('Showing residual maps and tclean masks, stopping criteria, and thresholds for ')
        print(*allcombires, sep = "\n")
        print(' ')      
        
        for i in range(0, len(allcombitxt)):
            os.system('rm -rf ' + allcombires[i] + '.fits')
            os.system('rm -rf ' + allcombimask[i] + '.fits')
            cta.exportfits(imagename=allcombires[i], fitsimage=allcombires[i] + '.fits', dropdeg=True)
            cta.exportfits(imagename=allcombimask[i], fitsimage=allcombimask[i] + '.fits', dropdeg=True)
            tcleanresults = dc.file_to_pydict2(allcombitxt[i])
            dc.pydict_to_file(tcleanresults, allcombitxt[i])       # export to human readable format 
            #print(tcleanresults['threshold'])
            stop_crit.append(tcleanresults['stopcode'])
            cleanthresh.append(tcleanresults['threshold'])
            cleaniterdone.append(tcleanresults['iterdone'])
        
        #allcombiresfits = [a.replace('.residual','.residual.fits') for a in allcombires]
        #allcombimaskfits = [a.replace('.mask','.mask.fits') for a in allcombimask]
        
        #labelnames
        allcombireslabel = [a.replace(pathtoimage+sourcename+cleansetup+'.','') for a in allcombitxt]
        
    
        iqa.show_residual_maps(allcombires, allcombimask,
                              channel=mapchan, 
                              save=True, 
                              plotname=assessment+'/Residual_maps_'+sourcename+cleansetup+steplist, 
                              labelname=allcombireslabel,
                              titlename='Residual maps in channel '+str(mapchan)+' from the tclean instances used by the chosen \n  combination methods for '+sourcename+cleansetup,
                              stop_crit=stop_crit,
                              cleanthresh=cleanthresh,
                              cleaniterdone=cleaniterdone)                                    
    
    
    
    #tcleanims = ['/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.image']
    #featherims = ['/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.feather_f1.0.image']
    #SSCims = ['/data/moser/data_combi/DC/DC_Ly_tests//pointGauss/BGauss_3L.SSC_f1.0.image']


    
    ########## Assessment with respect to SD image ############
    
    os.system('rm -rf ' + sdroregrid + '.fits')
    cta.exportfits(imagename=sdroregrid, fitsimage=sdroregrid + '.fits', dropdeg=True)
    
    allcombims0 = tcleanims  + featherims + SSCims     + hybridims  + sdintims  + TP2VISims
    #print(allcombims)
    print(' ')
    print(' ')
    print('Running assessment with respect to SD image on ')
    print(*allcombims0, sep = "\n")
    print(' ')
    
    
    allcombims = [a.replace('.image','.image.pbcor') for a in allcombims0]
    allcombpbs = [a.replace('.image','.pb') for a in allcombims0]
    allcombimsfits = [a.replace('.image.pbcor','.image.pbcor.fits') for a in allcombims]
    
    # make comparison plots
    
    #labelnames
    allcombi = [a.replace(pathtoimage+sourcename+cleansetup+'.','').replace('.image.pbcor','') for a in allcombims]
    

    # show combi products
    
    combitoplot=allcombims.copy()
    labeltoplot=allcombi.copy()
    
    combitoplot.append(sdroregrid)
    labeltoplot.append('SD image')
    #print('combitoplot', combitoplot)
    #print('labeltoplot', labeltoplot)    
    
    
    # what to do, if there are more than 4 plots (=max per page) to do 
    # allowed number of plots in IQA function
    nplt=4
    intdiv=int(len(combitoplot)/nplt)
    mod=len(combitoplot)%nplt  
 

    combitoploti=[]
    labeltoploti=[]
    
    for n in range(0,intdiv):
        combitoploti.append(combitoplot[n*nplt+0:n*nplt+nplt])
        labeltoploti.append(labeltoplot[n*nplt+0:n*nplt+nplt])
    combitoploti.append(combitoplot[intdiv*nplt+0:intdiv*nplt+mod])
    labeltoploti.append(labeltoplot[intdiv*nplt+0:intdiv*nplt+mod])
    #print('combitoploti', combitoploti)
    #print('labeltoploti', labeltoploti)
 
 
    if mapchan==None:
        chan=0
    else:
        chan = mapchan  
        
    for i in range(0,len(combitoploti)):
        iqa.show_combi_maps(combitoploti[i], #allcombimask,
                              channel=chan, 
                              save=True, 
                              plotname=assessment+'/Combined_maps_'+sourcename+cleansetup+steplist+'_'+str(i), 
                              labelname=labeltoploti[i],
                              titlename='Combined maps in channel '+str(mapchan)+' from the chosen \n  combination methods for '+sourcename+cleansetup+'_'+str(i)
                          )    
    
    
    
    
    # make Apar and fidelity images
   
    #print(sdroregrid)
    #print(allcombims)   
    

    iqa.get_IQA(ref_image = sdroregrid, target_image=allcombims, 
                pb_image=allcombpbs[0], masking_RMS=image_rms, 
                target_beam_index=0) #, pbval=pbval)
    
    
    
     
    
    
    if mode=='cube':   
        iqa.Compare_Apar_cubes(ref_image = sdroregrid, 
                               target_image=allcombims,
                               save=True,
                               plotname=assessment+'/SD_Apar_channels_'+sourcename+cleansetup+steplist,
                               labelname=allcombi, 
                               titlename='Apar Parameter of cube: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.','')
                               )
        iqa.Compare_Fidelity_cubes(ref_image = sdroregrid, 
                               target_image=allcombims,
                               save=True,
                               plotname=assessment+'/SD_Fidelity_channels_'+sourcename+cleansetup+steplist,
                               labelname=allcombi, 
                               titlename='Fidelity of cube: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.','')
                               )      
            
        for i in range(0,len(allcombims)):
            os.system('rm -rf ' + allcombims[i]+'.mom0')
            os.system('rm -rf ' + allcombims0[i]+'_clipped*')
            # sigma clipped moment maps
            cta.immath(imagename=allcombims0[i],
                   expr='IM0[IM0>'+str(image_rms)+']', 
                   outfile=allcombims0[i]+'_clipped')            
            cta.immath(imagename=[allcombims0[i]+'_clipped', allcombpbs[i]],
                   expr='IM0/IM1', 
                   outfile=allcombims0[i]+'_clipped_pbcorr')             
            cta.immoments(imagename=allcombims0[i]+'_clipped_pbcorr',
                       moments=[0],                                           
                       chans=momchans,                                       
                       outfile=allcombims0[i]+'_clipped_pbcorr.mom0')
            # smoothing *'_clipped_pbcorr.mom0' gives much lower flux value than it should --> use its minimum value for masking mom0 in get_IQA        
            imrms_mom0min = cta.imstat(allcombims0[i]+'_clipped_pbcorr.mom0')['min'][0]           
            cta.immoments(imagename=allcombims[i],
                       moments=[0],                                           
                       chans=momchans, #includepix=[image_rms, 10000000000.0],                                        
                       outfile=allcombims[i]+'.mom0')                       
            os.system('rm -rf ' + allcombims[i]+'.mom0.fits')
            cta.exportfits(imagename=allcombims[i]+'.mom0', fitsimage=allcombims[i]+'.mom0.fits', dropdeg=True)
            midchan=int(general_tclean_param['nchan']/2)
            os.system('rm -rf ' + allcombpbs[i]+'.chan'+str(midchan))
            cta.immath(imagename=[allcombpbs[i]],
                   expr='IM0', chans=str(midchan),
                   outfile=allcombpbs[i]+'.chan'+str(midchan))
            os.system('rm -rf ' + allcombpbs[i]+'.chan'+str(midchan)+'.fits')
            cta.exportfits(imagename=allcombpbs[i]+'.chan'+str(midchan), fitsimage=allcombpbs[i]+'.chan'+str(midchan)+'.fits', dropdeg=True)

            #mapchan=general_tclean_param['nchan']/2.
            iqa.show_Apar_map(    sdroregrid,allcombims[i],
                                  channel=mapchan, 
                                  save=True, 
                                  plotname=assessment+'/SD_Apar_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor','')+'_channel', #expecting only one file name entry per combi-method
                                  labelname=allcombi[i],
                                  titlename='Apar map in channel '+str(mapchan)+' for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+sdroregrid.replace(pathtoimage,''))                                    
           
            iqa.show_Fidelity_map(sdroregrid,
                                  allcombims[i],
                                  channel=mapchan, 
                                  save=True, 
                                  plotname=assessment+'/SD_Fidelity_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor','')+'_channel', #expecting only one file name entry per combi-method
                                  labelname=allcombi[i],
                                  titlename='Fidelity map in channel '+str(mapchan)+' for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+sdroregrid.replace(pathtoimage,''))                                    
       
        os.system('rm -rf ' + sdroregrid+'.mom0')  
        # no sigma clipped moment maps - no measurement implemented yet
        cta.immoments(imagename=sdroregrid,
                   moments=[0],                                           
                   chans=momchans,                                         
                   outfile=sdroregrid+'.mom0')
        
       
        
        
        # use mom0-maps as input for the cont-defined Apar/fidelity functions
        allcombims = [a.replace('.image.pbcor', '.image.pbcor.mom0') for a in allcombims]
        allcombimsfits = [a.replace('.image.pbcor.mom0','.image.pbcor.mom0.fits') for a in allcombims]
    
        sdroregrid = sdroregrid+'.mom0'
        os.system('rm -rf ' + sdroregrid + '.fits')
        cta.exportfits(imagename=sdroregrid, fitsimage=sdroregrid + '.fits', dropdeg=True)
    
    
        # show combi products
        
        combitoplot=allcombims.copy()
        labeltoplot=allcombi.copy()
        
        combitoplot.append(sdroregrid)
        labeltoplot.append('SD image')

        # what to do, if there are more than 6 plots (=max per page) to do 
        intdiv=int(len(combitoplot)/nplt)
        mod=len(combitoplot)%nplt  
        
        combitoploti=[]
        labeltoploti=[]
        
        for n in range(0,intdiv):
            combitoploti.append(combitoplot[n*nplt+0:n*nplt+nplt])
            labeltoploti.append(labeltoplot[n*nplt+0:n*nplt+nplt])
        combitoploti.append(combitoplot[intdiv*nplt+0:intdiv*nplt+mod])
        labeltoploti.append(labeltoplot[intdiv*nplt+0:intdiv*nplt+mod])
        #print('combitoploti', combitoploti)
        #print('labeltoploti', labeltoploti)
        
        # plot 
        for i in range(0,len(combitoploti)):
            iqa.show_combi_maps(combitoploti[i], #allcombimask,
                                  channel=0, 
                                  save=True, 
                                  plotname=assessment+'/Combined_mom0_maps_'+sourcename+cleansetup+steplist+'_'+str(i), 
                                  labelname=labeltoploti[i],
                                  titlename='Combined maps in moment 0 from the chosen \n  combination methods for '+sourcename+cleansetup+'_'+str(i)
                              )    

        #image_rms = 10.*imrms_mom0min   # use minimum value of moment 0 map of image_rms-clipped cube as new mask threshold
        
        nchans4mom0=int(momchans.split('~')[1])-int(momchans.split('~')[0])  
        image_rms = 10.* np.sqrt(float(nchans4mom0)) * image_rms   # use old image_rms threshold + error porpagation times an arbitry factor (10.)
        iqa.get_IQA(ref_image = sdroregrid, target_image=allcombims, 
                     pb_image=allcombpbs[0]+'.chan'+str(midchan), masking_RMS=image_rms, 
                     target_beam_index=0) #, pbval=pbval)
    
     
    
    
    
      
              
    
    
    # all Apar and fidelity plots
    iqa.Compare_Apar(ref_image = sdroregrid, 
                     target_image=allcombims, 
                     save=True, 
                     plotname=assessment+'/SD_AparALL_'+sourcename+cleansetup+steplist,
                     labelname=allcombi, 
                     titlename='Apar Parameter: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))
    iqa.Compare_Fidelity(ref_image = sdroregrid, 
                     target_image=allcombims,
                     save=True, 
                     plotname=assessment+'/SD_FidelityALL_'+sourcename+cleansetup+steplist,
                     labelname=allcombi, 
                     titlename='Fidelity: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))      
    iqa.Compare_Flux_signal(ref_image = sdroregrid, 
                     target_image=allcombims,
                     save=True,
                     plotname=assessment+'/SD_FluxALL_'+sourcename+cleansetup+steplist,
                     labelname=allcombi,
                     titlename='Flux: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                    
    for i in range(0,len(allcombims)):
        # Apar and fidelity vs signal plots
        iqa.Compare_Apar_signal(ref_image = sdroregrid, 
                                 target_image=[allcombims[i]],
                                 save=True,
                                 noise=0.0, 
                                 plotname=assessment+'/SD_Apar_signal_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                 labelname=[allcombi[i]],
                                 titlename='Apar vs. Signal for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
        iqa.Compare_Fidelity_signal(ref_image = sdroregrid, 
                                 target_image=[allcombims[i]],
                                 save=True,
                                 noise=0.0, 
                                 plotname=assessment+'/SD_Fidelity_signal_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                 labelname=[allcombi[i]],
                                 titlename='Fidelity vs. Signal for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                                    
        iqa.Compare_Flux_signal(ref_image = sdroregrid, 
                                 target_image=[allcombims[i]],
                                 save=True,
                                 noise=0.0, 
                                 plotname=assessment+'/SD_Flux_signal_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                 labelname=[allcombi[i]],
                                 titlename='Flux vs. Signal for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))
        # Apar and fidelity image plots
        iqa.show_Apar_map(    sdroregrid,allcombims[i],
                              channel=0, 
                              save=True, 
                              plotname=assessment+'/SD_Apar_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                              labelname=allcombi[i],
                              titlename='Apar map for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+sdroregrid.replace(pathtoimage,''))                                    
    
        iqa.show_Fidelity_map(sdroregrid,
                              allcombims[i],
                              channel=0, 
                              save=True, 
                              plotname=assessment+'/SD_Fidelity_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                              labelname=allcombi[i],
                              titlename='Fidelity map for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+sdroregrid.replace(pathtoimage,''))                                    
    
    
    allcombimsfits_Apar = copy.deepcopy(allcombimsfits)  # Because Apar PS should not include reference
    allcombi_Apar = copy.deepcopy(allcombi)

    allcombimsfits.append(sdroregrid + '.fits')
    allcombi.append('single dish')
         
    #<- Removed. IT doesn make sense to compare images that are not at the same resolution    
    #iqa.genmultisps(allcombimsfits, save=True, 
    #               plotname=assessment+'/SD_Power_spectra_'+sourcename+cleansetup+steplist,
    #               labelname=allcombi,
    #               titlename='Power spectra for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
    
    allcombimsfits_conv = [a.replace('pbcor.fits','pbcor_convo2ref.fits') for a in allcombimsfits]
    #<- only for cubes, right?
    if mode=='cube': 
            allcombimsfits_conv = [a.replace('pbcor.mom0.fits','pbcor.mom0_convo2ref.fits') for a in allcombimsfits]
    #<-
    iqa.genmultisps(allcombimsfits_conv, save=True, 
                   plotname=assessment+'/SD_Power_spectra_convo2ref_'+sourcename+cleansetup+steplist,
                   labelname=allcombi,
                   titlename='Power spectra (convolved to SD) for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
    
    #<-Replacement
    ##allcombimsfits_conv_Apar = [a.replace('_convo2ref.fits','_convo2ref_Apar.fits') for a in allcombimsfits_conv]
    allcombimsfits_conv_Apar = [a.replace('pbcor.fits','pbcor_convo2ref_Apar.fits') for a in allcombimsfits_Apar]
    
    iqa.genmultisps(allcombimsfits_conv_Apar, save=True, 
                   plotname=assessment+'/SD_Power_spectra_convo2ref_Apar_'+sourcename+cleansetup+steplist,
                   #<-
                   ##labelname=allcombi,
                   labelname=allcombi_Apar,
                   #<-
                   titlename='Apar power spectra (convolved to SD) for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
    
    
    
    #################### NOT YET WORKING !!! problems #######
    #
    #iqa.get_aperture(allcombimsfits,position=(1,1),Nbeams=10)
    #
    ##### !!!needs SD-fitsfile ----> to create in step 1 !!!!
    
    
    
    
    
    
    if skymodel!='':
    
        ########## Assessment with respect to SKYMODEL image ############
        
        #os.system('rm -rf ' + sdroregrid + '.fits')
        #cta.exportfits(imagename=sdroregrid, fitsimage=sdroregrid + '.fits', dropdeg=True)
        
        if mode=='cube':   
            allcombims0 = tcleanims  + featherims + SSCims     + hybridims  + sdintims  + TP2VISims   # need to fix TP2VIS for cont images without emission-free region first 
        else:
            print('Skip TP2VIS results in this selection - most likely no good result in mfs-mode')
            allcombims0 = tcleanims  + featherims + SSCims     + hybridims  + sdintims  #+ TP2VISims   # need to fix TP2VIS for cont images without emission-free region first 
        #print(allcombims)
        print(' ')
        print(' ')
        print('Running assessment with respect to the SKYMODEL on ')
        print(*allcombims0, sep = "\n")
        print(' ')
    
        
        allcombims = [a.replace('.image','.image.pbcor') for a in allcombims0]
        allcombimsfits = [a.replace('.image.pbcor','.image.pbcor.fits') for a in allcombims]
        
        
        
        # make comparison plots
        
        #### imbase         = pathtoimage + 'skymodel-b_120L
        #sourcename = imbase.replace(pathtoimage,'')
        # folder to put the assessment images to 
        #assessment=pathtoimage + 'assessment_'+sourcename+cleansetup
        #os.system('mkdir '+assessment) 
        
        
        #labelnames
        allcombi = [a.replace(pathtoimage+sourcename+cleansetup+'.','').replace('.image.pbcor','') for a in allcombims]
        
        
        ## step numbers 
        #thesteps2 = map(str, thesteps)    
        #stepsjoin=''.join(thesteps2)
        #steps=stepsjoin.replace('0','').replace('1','').replace('8','')
        #steplist='_s'+steps
        
        
        # get largest beam axes present in the input images and smooth model image to them
        
        BeamMaj=[]
        BeamMin=[]
        BeamPA =[]
        
        # expects common beam and not perplanebeam @cube!
         
        for j in range(0,len(allcombims)): 
            BeamMaj.append(cta.imhead(allcombims[j], mode='get', hdkey='bmaj')['value'])
            BeamMin.append(cta.imhead(allcombims[j], mode='get', hdkey='bmin')['value'])
            BeamPA.append(cta.imhead(allcombims[j], mode='get', hdkey='bpa' )['value'])
    
        print(BeamMaj)
        print(BeamMin) 
        print(BeamPA )
        
        skymodelreg=imbase +'.skymodel.regrid'
        os.system('rm -rf '+skymodelreg)
        dc.regrid_SD(skymodel, skymodelreg, allcombims[0])

        os.system('rm -rf ' + skymodelreg + '.fits')
        cta.exportfits(imagename=skymodelreg, fitsimage=skymodelreg + '.fits', dropdeg=True)
            
        skymodelconv=imbase +'.skymodel.regrid.conv'
        os.system('rm -rf '+skymodelconv+'*')

        cta.imsmooth(imagename = skymodelreg,
                     kernel    = 'gauss',               
                     targetres = True,                                                             
                     major     = str(max(np.array(BeamMaj))*1.1)+'arcsec', 
                     minor     = str(max(np.array(BeamMin))*1.1)+'arcsec',    
                     pa        = str(np.mean(np.array(BeamPA)))+'deg',                                       
                     outfile   = skymodelconv,            
                     overwrite = True)    
        # have to add 10% in size (factor 1.1), else imsmooth in get_IQA might fail for largest beam size in image set                                              
        
        
        
        os.system('rm -rf ' + skymodelconv + '.fits')
        cta.exportfits(imagename=skymodelconv, fitsimage=skymodelconv + '.fits', dropdeg=True)
                

        # show combi products
        
        combitoplot=allcombims.copy()
        labeltoplot=allcombi.copy()

        combitoplot.append(sdroregrid.replace('.mom0','')) # watch out for changes in the variable! who is at this stage of the script in - mom0 or the cube?
        labeltoplot.append('SD image')

        combitoplot.append(skymodelreg)
        labeltoplot.append('model')
        
        combitoplot.append(skymodelconv)
        labeltoplot.append('convolved model')


        #print('combitoplot', combitoplot)
        #print('labeltoplot', labeltoplot)    
        
        #if len(combitoplot)>6:
        

        # what to do, if there are more than 4 plots (=max per page) to do 

        intdiv=int(len(combitoplot)/nplt)
        mod=len(combitoplot)%nplt  
        
        
        combitoploti=[]
        labeltoploti=[]
        
        for n in range(0,intdiv):
            combitoploti.append(combitoplot[n*nplt+0:n*nplt+nplt])
            labeltoploti.append(labeltoplot[n*nplt+0:n*nplt+nplt])
        combitoploti.append(combitoplot[intdiv*nplt+0:intdiv*nplt+mod])
        labeltoploti.append(labeltoplot[intdiv*nplt+0:intdiv*nplt+mod])
        #print('combitoploti', combitoploti)
        #print('labeltoploti', labeltoploti)
        
        for i in range(0,len(combitoploti)):
            iqa.show_combi_maps(combitoploti[i], #allcombimask,
                                  #channel=mapchan, 
                                  channel=chan, 
                                  save=True, 
                                  plotname=assessment+'/Combined_maps_'+sourcename+cleansetup+steplist+'_model_'+str(i), 
                                  labelname=labeltoploti[i],
                                  titlename='Combined maps in channel '+str(mapchan)+' from the chosen \n  combination methods for '+sourcename+cleansetup+'_'+str(i)
                              )    
        



        
        # make Apar and fidelity images
        
        iqa.get_IQA(ref_image = skymodelconv, target_image=allcombims, 
                    pb_image=allcombpbs[0], masking_RMS=image_rms, 
                    target_beam_index=0) #, pbval=pbval)
   
        
        
        
         
        
        
        if mode=='cube':   
            iqa.Compare_Apar_cubes(ref_image = skymodelconv, 
                                   target_image=allcombims,
                                   save=True,
                                   plotname=assessment+'/Model_Apar_channels_'+sourcename+cleansetup+steplist,
                                   labelname=allcombi, 
                                   titlename='Apar Parameter of cube: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.','')
                                   )
            iqa.Compare_Fidelity_cubes(ref_image = skymodelconv, 
                                   target_image=allcombims,
                                   save=True,
                                   plotname=assessment+'/Model_Fidelity_channels_'+sourcename+cleansetup+steplist,
                                   labelname=allcombi, 
                                   titlename='Fidelity of cube: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.','')
                                   )      
                
            for i in range(0,len(allcombims)):
                #os.system('rm -rf ' + allcombims[i]+'.mom0')
                #cta.immoments(imagename=allcombims[i],
                #           moments=[0],                                           
                #           chans=momchans,                                         
                #           outfile=allcombims[i]+'.mom0')
                #os.system('rm -rf ' + allcombims[i]+'.mom0.fits')
                #cta.exportfits(imagename=allcombims[i]+'.mom0', fitsimage=allcombims[i]+'.mom0.fits', dropdeg=True)
                #mapchan=general_tclean_param['nchan']/2.
                iqa.show_Apar_map(    skymodelconv,allcombims[i],
                                      channel=mapchan, 
                                      save=True, 
                                      plotname=assessment+'/Model_Apar_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor','')+'_channel', #expecting only one file name entry per combi-method
                                      labelname=allcombi[i],
                                      titlename='Apar map in channel '+str(mapchan)+' for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+skymodelconv.replace(pathtoimage,''))                                    
               
                iqa.show_Fidelity_map(skymodelconv,
                                      allcombims[i],
                                      channel=mapchan, 
                                      save=True, 
                                      plotname=assessment+'/Model_Fidelity_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor','')+'_channel', #expecting only one file name entry per combi-method
                                      labelname=allcombi[i],
                                      titlename='Fidelity map in channel '+str(mapchan)+' for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+skymodelconv.replace(pathtoimage,''))                                    
           
            os.system('rm -rf ' + skymodelconv+'.mom0')               
            cta.immoments(imagename=skymodelconv,
                       moments=[0],                                           
                       chans=momchans,                                         
                       outfile=skymodelconv+'.mom0')

            
           
            
            
            # use mom0-maps as input for the cont-defined Apar/fidelity functions
            allcombims = [a.replace('.image.pbcor', '.image.pbcor.mom0') for a in allcombims]
            allcombimsfits = [a.replace('.image.pbcor.mom0','.image.pbcor.mom0.fits') for a in allcombims]
        
            skymodelconv = skymodelconv+'.mom0'
            os.system('rm -rf ' + skymodelconv + '.fits')
            cta.exportfits(imagename=skymodelconv, fitsimage=skymodelconv + '.fits', dropdeg=True)
      
            # show combi products
            
            combitoplot=allcombims.copy()
            labeltoplot=allcombi.copy()
            
            combitoplot.append(sdroregrid)
            labeltoplot.append('SD image')
            
            combitoplot.append(skymodelreg)
            labeltoplot.append('model')
            
            combitoplot.append(skymodelconv)
            labeltoplot.append('convolved model')
            
            # what to do, if there are more than 6 plots (=max per page) to do 
            intdiv=int(len(combitoplot)/nplt)
            mod=len(combitoplot)%nplt  
            
            combitoploti=[]
            labeltoploti=[]
            
            for n in range(0,intdiv):
                combitoploti.append(combitoplot[n*nplt+0:n*nplt+nplt])
                labeltoploti.append(labeltoplot[n*nplt+0:n*nplt+nplt])
            combitoploti.append(combitoplot[intdiv*nplt+0:intdiv*nplt+mod])
            labeltoploti.append(labeltoplot[intdiv*nplt+0:intdiv*nplt+mod])
            #print('combitoploti', combitoploti)
            #print('labeltoploti', labeltoploti)
            
            # plot 
            for i in range(0,len(combitoploti)):
                iqa.show_combi_maps(combitoploti[i], #allcombimask,
                                      channel=0, 
                                      save=True, 
                                      plotname=assessment+'/Combined_mom0_maps_'+sourcename+cleansetup+steplist+'_model_'+str(i), 
                                      labelname=labeltoploti[i],
                                      titlename='Combined maps in moment 0 from the chosen \n  combination methods for '+sourcename+cleansetup+'_'+str(i)
                                  )    
            
            
            
  
            iqa.get_IQA(ref_image = skymodelconv, target_image=allcombims, 
                        pb_image=allcombpbs[0]+'.chan'+str(midchan), masking_RMS=image_rms, 
                        target_beam_index=0) #, pbval=pbval)
         
        
        
        
          
                  
        
        
        # all Apar and fidelity plots
        iqa.Compare_Apar(ref_image = skymodelconv, 
                         target_image=allcombims, 
                         save=True, 
                         plotname=assessment+'/Model_AparALL_'+sourcename+cleansetup+steplist,
                         labelname=allcombi, 
                         titlename='Apar Parameter: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))
        iqa.Compare_Fidelity(ref_image = skymodelconv, 
                         target_image=allcombims,
                         save=True, 
                         plotname=assessment+'/Model_FidelityALL_'+sourcename+cleansetup+steplist,
                         labelname=allcombi, 
                         titlename='Fidelity: comparison for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
        for i in range(0,len(allcombims)):
            # Apar and fidelity vs signal plots
            iqa.Compare_Apar_signal(ref_image = skymodelconv, 
                                     target_image=[allcombims[i]],
                                     save=True,
                                     noise=0.0, 
                                     plotname=assessment+'/Model_Apar_signal_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                     labelname=[allcombi[i]],
                                     titlename='Apar vs. Signal for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
            iqa.Compare_Fidelity_signal(ref_image = skymodelconv, 
                                     target_image=[allcombims[i]],
                                     save=True,
                                     noise=0.0, 
                                     plotname=assessment+'/Model_Fidelity_signal_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                     labelname=[allcombi[i]],
                                     titlename='Fidelity vs. Signal for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                                    
            # Apar and fidelity image plots
            iqa.show_Apar_map(    skymodelconv,
                                  allcombims[i],
                                  channel=0, 
                                  save=True, 
                                  plotname=assessment+'/Model_Apar_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                  labelname=allcombi[i],
                                  titlename='Apar map for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+sdroregrid.replace(pathtoimage,''))                                    
        
            iqa.show_Fidelity_map(skymodelconv,
                                  allcombims[i],
                                  channel=0, 
                                  save=True, 
                                  plotname=assessment+'/Model_Fidelity_map_'+allcombims[i].replace(pathtoimage,'').replace('.image.pbcor',''), #expecting only one file name entry per combi-method
                                  labelname=allcombi[i],
                                  titlename='Fidelity map for \ntarget: '+allcombims[i].replace(pathtoimage,'')+' and \nreference: '+sdroregrid.replace(pathtoimage,''))                                    
        
        
        
        allcombimsfits.append(skymodelconv + '.fits')
        allcombi.append('model')
        
        iqa.genmultisps(allcombimsfits, save=True, 
                       plotname=assessment+'/Model_Power_spectra_'+sourcename+cleansetup+steplist,
                       labelname=allcombi,
                       titlename='Power spectra for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
            
        allcombimsfits_conv = [a.replace('pbcor.fits','pbcor_convo2ref.fits') for a in allcombimsfits]
        allcombimsfits_conv = [a.replace('pbcor.mom0.fits','pbcor.mom0_convo2ref.fits') for a in allcombimsfits]
         
    
        iqa.genmultisps(allcombimsfits_conv, save=True, 
                       plotname=assessment+'/Model_Power_spectra_convo2ref_'+sourcename+cleansetup+steplist,
                       labelname=allcombi,
                       titlename='Power spectra (convolved to model) for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
        
        allcombimsfits_conv_Apar = [a.replace('_convo2ref.fits','_convo2ref_Apar.fits') for a in allcombimsfits_conv]
    
        iqa.genmultisps(allcombimsfits_conv_Apar, save=True, 
                       plotname=assessment+'/Model_Power_spectra_convo2ref_Apar_'+sourcename+cleansetup+steplist,
                       labelname=allcombi,
                       titlename='Apar power spectra (convolved to model) for \nsource: '+sourcename+' and \nclean setup: '+cleansetup.replace('.',''))                         
            
    
    
        #################### NOT YET WORKING !!! problems #######
        #
        #iqa.get_aperture(allcombimsfits,position=(1,1),Nbeams=10)
        #
        ##### !!!needs SD-fitsfile ----> to create in step 1 !!!!
        
    print('###')    
    print('### Assessment: ' +clip_string)
    print('### Clean threshold was', general_tclean_param['threshold'])
    if mode=='cube':   
        print('### Mom0-Assessment cut-off', image_rms)  #NOTE: not the initial input but rederived for mom0!
    #print('### Clipping level for the assessment of the maps was at %.6f Jy/beam' %image_rms)       
    print('###')    
    
    


    
    
    


# delete tclean TempLattices

os.system('rm -rf '+pathtoimage + 'TempLattice*')


end = time.time()
diff = round(end - start)


filename0 = imbase + cleansetup +'._Runtime_' + steplist2

if dryrun==False:
    filename = filename0
if dryrun==True:
    filename = filename0+'_assessment'

os.system('rm -rf '+filename+'.txt')
string1 = 'Execution of steps '+str(thesteps)[1:-1]+' of DC_run.py with dryrun='+str(dryrun)+' took:'
string2 = str(diff) + ' seconds = ' + str(round(diff/60.0, 2)) + ' minutes = ' + str(round(diff/60.0/60.0, 2)) + ' hours'
f = open(filename+'.txt','w')
f.write(string1)
f.write('\n'+string2)
f.close()

print('')
print('')
print('---------------------------- WE ARE DONE! -----------------------------')
print('')
print(string1)
print(string2)


