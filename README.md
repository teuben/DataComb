# Data Combination Project

1. If you want to get an image go to quick_start.md,
2. if you want to understand the steps go to Overview.md,
3. if you are more advanced and want to start playing with the parameters to hone in your data combination go to DC_pars?

General overview.md
X Preparation.md (only once)
Quick_start.md
DC_pars.md – link to Template_pars.py and explain
DC_run.md










# Scripts for the Paper

These should be the steps that allow you to reproduce the
figures in the paper:

1. Ensure your CASA has **astropy** installed
2. Ensure the **analysisUtilities** are installed for your CASA
3. Run configure to be able to run the CASA based scripts
4. Gather the data (see data/README.md)
5. Execfile DC_script.py to run through your selected data set


   
## 1. - 3. Preparations
Details are given in [Preparation](https://github.com/teuben/DataComb/blob/master/Preparation.md)
You have to make these adjustments just once.


## 4. Data

Details are in [data/README.md](data/README.md)

This suggests that the data is present in **data**, physically or via
a (sym)link.   Example:


       wget https://ftp.astro.umd.edu/pub/teuben/DC2019/skymodel-b.fits 
       wget https://ftp.astro.umd.edu/pub/teuben/DC2019/skymodel-c.fits
       curl https://ftp.astro.umd.edu/pub/teuben/DC2019/skymodel-b.sim.tar | tar xf -
       curl https://ftp.astro.umd.edu/pub/teuben/DC2019/skymodel-c.sim.tar | tar xf -


## 5. DC_script.py, DC_run.py, and IQA_script.py

At each start of a CASA instance you have to call the **DC_locals.py**
once to set up your source and destination folders, e.g.

    execfile("/home/teuben/DataComb/DC_locals.py",globals())

**DC_script.py** is a wrapper that calls the **DC_pars**-file you
  defined in there and then the combination program **DC_run.py**.

Alternatively, you can call

	execfile("/home/teuben/DataComb/DC_pars_M100.py", globals()) 
	execfile("/home/teuben/DataComb/DC_run.py",globals())

An overview of the capabilities of **DC_run.py** is given in [Overview](Overview.md) 
and in more detail in [DC_run](DC_run.md).
A quick start guide is given in	[Quick_start](Quick_start.md).

**DC_run.py** uses the python module **datacomb.py** for preparation and combination 
of the data and the python module **IQA_script.py** for the assessment of the combination products. 
Both modules can be used as a stand-alone.


