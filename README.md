# Data Combination Project

1. If you want to (more quickly) get combined images, go directly to [Quick_start.md](Quick_start.md),
2. If you want to understand the steps, go to [Overview.md](Overview.md),
3. [Advanced users] If you want adjust parameters and perform data combination on your own data, go to [DC_pars.md](DC_pars.md).


# Scripts for the Paper

These should be the steps that allow you to reproduce the data combination as presented in Plunkett et al. (2023):

1. Ensure your CASA has **astropy** installed
2. Ensure the **analysisUtilities** are installed for your CASA
3. Run configure to be able to run the CASA based scripts
4. Gather the data (see data/README.md)
5. Execfile DC_script.py to run through your selected data set


   
## 1. - 3. Preparations
Details are given in [Preparation](https://github.com/teuben/DataComb/blob/master/Preparation.md). 

You have to make these adjustments *just once*.  Steps include:

1. Requirements
2. Configure
3. (Optional but Recommended) Permanently Set Up Your CASA Environment



## 4. Data

Details are in [data/README.md](data/README.md). 

As suggested in [Preparation](Preparation.md), the setup assumes that the data is present in **data**, physically or via a (sym)link.  If you cloned this Github repository, then the **data** directory should already exist.  You can modify this for your system as needed.

## 5. DC_script.py, DC_run.py, and IQA_script.py

At each start of a CASA instance you have to call the **DC_locals.py**
once to set up your source and destination folders, e.g.

    execfile("/home/teuben/DataComb/DC_locals.py",globals())

**DC_script.py** is simply a wrapper that first calls the **DC_pars**-file you
  designate there, and then the combination program **DC_run.py**.

Alternatively, you can use these two lines to call:

	execfile("/home/teuben/DataComb/DC_pars.py", globals()) 
	execfile("/home/teuben/DataComb/DC_run.py",globals())

For more on **DC_run.py**, you can find an overview of the capabilities given in [Overview](Overview.md), 
and more detail in [DC_run](DC_run.md).  Templates of **DC_pars**-files are found in the templates directory.

**DC_run.py** uses the Python module **datacomb.py** for preparation and combination 
of the data, and the Python module **IQA_script.py** for the assessment of the combination products. 
Both modules can be used as a stand-alone.

A quick start guide is given in	[Quick_start](Quick_start.md).


