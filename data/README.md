# Dataset that have been used for DataComb

1) M100 (casaguides)          
2) Skymodel GMC fractal/powerspectrum (Koda) 

Two datasets marked by a '*' did not get used, although "papersky" was available and was tested
by some that it worked. The SDINT method that was 


1) M100 from casaguides
   --------------------

The https://casaguides.nrao.edu/index.php/M100_Band3_Combine_5.4 casaguide walks you through
a feather combination. We will also try to provide this example for the other combination
methods.


To get the full data, see also https://casaguides.nrao.edu/index.php/M100_Band3#Obtaining_the_Data

For EA use:  https://alma-dl.mtk.nao.ac.jp/ftp/alma/sciver/
    EU use:  https://almascience.eso.org/almadata/sciver/
    NA use:  https://bulk.cv.nrao.edu/almadata/sciver/

For 12m use directory:     M100Band3_12m
For 7m/TP use directory:   M100Band3ACA

you will need the 12m, 7m and TP data, e.g. in NA (replace the stem of the URL with the EU/EA ones)

  wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3_12m/M100_Band3_12m_CalibratedData.tgz
  wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_7m_CalibratedData.tgz
  wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_ACA_ReferenceImages_5.1.tgz

This totals 24GB and we will have this on a USB.

An alternative can be a single large tar file

  wget https://ftp.astro.umd.edu/pub/teuben/DC2019/M100_big.tar

if the archives are too cumbersome.



We are also planning on a trimmed version of these big data to immediately jump into data combination.
See http://admit.astro.umd.edu/~teuben/QAC/qac_bench5.tar.gz with trimmed M100 data, good for the
QAC benchmark. These are the gridded to the 70 channels the TP data were available as.
Another reason for this trimmed version is to ensure that all data have been sorted correctly, as
some programs (certainly in the past) could not deal with sorted differently by frequency.

TP2VIS: https://github.com/tp2vis/distribute/blob/master/example1.md   needs to be updated


2) skymodel GMC fractal/powerspectrum (Koda)
   -----------------------------------------

The new 2020 link to the DC2019 data is via ftp or http (they are identical)

      https://ftp.astro.umd.edu/pub/teuben/DC2019
      https://ftp.astro.umd.edu/pub/teuben/DC2019/scripts4paper
      (local at UMD) /n/ftp/pub/teuben/DC2019

In here you will find the following files:

    skymodel-b.fits                  original skymodel plus two fuzzy "point" sources
    skymodel-c.fits                  skymodel with a different random seed, same powerlaw as 'b'
    skymodel-b.sim.tar               MS simulation files from Toshi (large: 7GB)
    skymodel-c.sim.tar	             MS sim files
    pointSrc_gaussOnly.sim.tar       MS sim files
    pointSrc_pointOnly.sim.tar       MS sim files
    pointSrc_pointSrcGauss.sim.tar   MS sim files
    qac_bench5.tar.gz                M100 data : 70 channels at 5 km/s for 12m, 7m and TP

Toshi's models are big, but best solved by placing them in dc2019/data as well (or a link)
Examples:

        gmcSkymodel/gmc_2L/                   an older - kind of wrong - but small < 1GB data for testing
        skymodel-b.sim/skymodel-b_120L        full 8GB multi-day dataset
        skymodel-c.sim/skymodel-c_120L        full 8GB multi-day dataset


You will find some old links (but same data) here:

http://admit.astro.umd.edu/~teuben/QAC/skymodel.fits
http://admit.astro.umd.edu/~teuben/QAC/skymodel-a.fits    
http://admit.astro.umd.edu/~teuben/QAC/skymodel-b.fits    
http://admit.astro.umd.edu/~teuben/QAC/skymodel-c.fits    
http://admit.astro.umd.edu/~teuben/QAC/skymodel-d.fits    
http://admit.astro.umd.edu/~teuben/QAC/skymodel.ptg     
http://admit.astro.umd.edu/~teuben/QAC/qac_bench5.tar.gz

These are from the old 4096 x 4096 models.  The skymodel.fits
is the original one, we added (two) 0.1 Jy point sources (see
header where) to check how well they are recoverable.

We have:
    skymodel-a.fits       original skymodel plus real point sources - not used
    skymodel-b.fits       original skymodel plus two fuzzy "point" sources
    skymodel-c.fits       skymodel with a different random seed, same powerlaw as 'b'
    skymodel-d.fits       skymodel with a different random seed, same powerlaw as 'b'
    skymodel-e.fits       skymodel with different powerlaw, same seed as 'c'

A newer 16k x 16k model, and associate pre-computed MS, available
here:

https://ftp.astro.umd.edu/pub/teuben/tp2vis/skymodel_16k.fits
https://ftp.astro.umd.edu/pub/teuben/tp2vis/tp2vis-sample2.tar.gz


Older data link:       https://ftp.astro.umd.edu/pub/teuben/DC2019/scripts4paper
