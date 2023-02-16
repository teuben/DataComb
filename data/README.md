# Dataset that have been used for DataComb (Plunkett et al. 2023)

1) M100 (from Casaguides)          
2) Skymodel GMC fractal/power spectrum (Koda et al. 2019) 
3) ... More datasets have been tested, and may be documented in the future


1) M100 (Casaguides)
   -----------------

The https://casaguides.nrao.edu/index.php/M100_Band3_Combine_6.2 Casaguide walks you through
a combination with Feather. We utilize the same dataset for Feather and for the other combination methods,
so they can be compared.

To get the full data, see https://casaguides.nrao.edu/index.php/M100_Band3#Obtaining_the_Data

For EA use:  https://alma-dl.mtk.nao.ac.jp/ftp/alma/sciver/
    EU use:  https://almascience.eso.org/almadata/sciver/
    NA use:  https://bulk.cv.nrao.edu/almadata/sciver/

For 12m use directory:     M100Band3_12m
For 7m/TP use directory:   M100Band3ACA

you will need the 12m, 7m and TP data, e.g. in NA (replace the stem of the URL with the EU/EA ones)

  wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3_12m/M100_Band3_12m_CalibratedData.tgz
  wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_7m_CalibratedData.tgz
  wget https://bulk.cv.nrao.edu/almadata/sciver/M100Band3ACA/M100_Band3_ACA_ReferenceImages_5.1.tgz

An alternative can be a single large tar file

  wget https://ftp.astro.umd.edu/pub/teuben/DataComb/M100_big.tar

if the archives are too cumbersome.



We are also planning on a trimmed version of these big data to immediately jump into data combination.
See http://admit.astro.umd.edu/~teuben/QAC/qac_bench5.tar.gz with trimmed M100 data, good for the
QAC benchmark. These are gridded to the same 70 channels corresponding to the TP data.
For testing purposes, another reason for this trimmed version is to ensure that all data have been sorted correctly, as
some programs (certainly in the past) could not deal with data sorted differently by frequency.


2) skymodel GMC fractal/powerspectrum (Koda)
   -----------------------------------------

The new (since 2022) link to the DataComb data is via ftp or http (they are identical)

      https://ftp.astro.umd.edu/pub/teuben/DataComb
      (local at UMD) /n/ftp/pub/teuben/DataComb

In here you will find the following files:

    skymodel-b.fits                  original skymodel plus two fuzzy "point" sources
    skymodel-c.fits                  skymodel with a different random seed, same powerlaw as 'b'
    skymodel-b.sim.tar               MS simulation files from Toshi (large: 7GB)
    skymodel-c.sim.tar	             MS sim files
    pointSrc_gaussOnly.sim.tar       MS sim files
    pointSrc_pointOnly.sim.tar       MS sim files
    pointSrc_pointSrcGauss.sim.tar   MS sim files
    qac_bench5.tar.gz                M100 data : 70 channels at 5 km/s for 12m, 7m and TP


The skymodel model data are big, but best solved by placing them in data as well (or a link)
Examples:

        gmcSkymodel/gmc_2L/                   an older - kind of wrong - but small < 1GB data for testing
        skymodel-b.sim/skymodel-b_120L        full 8GB multi-day dataset
        skymodel-c.sim/skymodel-c_120L        full 8GB multi-day dataset

Also note that the code to generate the simulations is available inside the dataset, with the
comment that these were produced with CASA 5.6.1.


A newer 16k x 16k model, and associate pre-computed MS, available
here:

https://ftp.astro.umd.edu/pub/teuben/tp2vis/skymodel_16k.fits
https://ftp.astro.umd.edu/pub/teuben/tp2vis/tp2vis-sample2.tar.gz

