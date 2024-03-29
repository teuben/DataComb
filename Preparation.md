# Necessary Preparation to Run Data Combination
Follow these instructions to get your environment setup to run data combination (`DC_script.py`). Theoretically you will only have to do these things once. First you will ensure that you have the required software and packages (CASA, astropy, analysisUtils) then configure your CASA environment.

## Step 1: Requirements

1. CASA 6
2. astropy within your CASA installation
3. analysisUtils

### 1. CASA

We now only support CASA v6. See also https://casa.nrao.edu/casa_obtaining.shtml

### 2. astropy

You can test if your CASA installation has astropy by

```bash
casa -c "import astropy"
```
If this failed, you will need to manually install it.  Since CASA has its own python, you can
install it using `pip3` from the CASA prompt (it is cumbersome to try this from the unix command line):

```plain
CASA <1>: !pip3 install astropy
```
If this results in some kind of permission related problem, you will need to ask the owner of CASA to do this. Just to be clear, we are using only python3 now, hence CASA 6. 

You can find more on installing astropy at [astropy:docs](https://docs.astropy.org/en/stable/install.html)

### 3. analysisUtils

[This CASA Guide](https://casaguides.nrao.edu/index.php/Analysis_Utilities) gives instructions on how to download and install analysisUtils. Here's an example of installing it:

```bash
cd ~/.casa
wget ftp://ftp.cv.nrao.edu/pub/casaguides/analysis_scripts.tar
tar -xf analysis_scripts.tar
```

As of January 2023, analysisUtils is available on [zenodo](https://zenodo.org/record/7502160) (DOI: 10.5281/zenodo.7502160).

Then add the following lines to your `~/.casa/startup.py` script:

```plain
import sys
import os
sys.path.append(os.environ['HOME'] + '/.casa/analysis_scripts')
import analysisUtils as au
```

**Note:** You need a relatively new (as of January 2023) version of analysisUtils, that is compatible with CASA 6, in order for the commands that we use in DataComb to work.  Try ```au.version()```. Version 2.6 has been tested to work.

## Step 2: Configure

Before running `DC_script.py`, you will first need to configure your CASA
environment to set the script, data, and working directories that the
scripts will use on your local machine, as opposed to the current
defaults (it will expect your data to be locally present). One
suggested solution is the use of the included `configure.` You need to
execute the `configure` script from the `scripts4paper` directory to
set the directories

1. in which you would like to save the output products (`--with-s4p-work`) and
2. where the data you want to combine is located (`--with-s4p-data`).

We recommend putting all datasets in one directory and all output
files and images in another, then you only have to run `configure`
once. For example, let's say you plan to work with the M100 and GMC
example datasets. You could have one directory for the input data
`/users/user/DataComb/data/` where you will have a M100 directory and
a GMC directory. And another for output files and images,
`/users/user/DataComb/output/` where you will have a M100 folder and a
GMC folder.

Then your configure statement would be

```bash
./configure --with-s4p-work=/users/user/DataComb/output --with-s4p-data=/users/user/DataComb/data
```

This will place your working files in `/users/user/DataComb/output/` and
set `/users/user/DataComb/data/` to be the directory where all the
input data are located (at least for the DataComb project). Use the
--help argument to find out what other options might be useful for
you.

`configure` will produce a file called `DC_locals.py` in the directory
that you run `configure` in - this should be the directory where
`DC_script.py` is.


**Note:**  Mac users may need to install the needed command `realpath` via "brew install coreutils" for configure to work. Pay attention if you see ```checking scripts4paper setup... ./configure: line 1751: realpath: command not found```

## Step 3: (Optional but Recommended) Permanently Set Up Your CASA Environment

We recommend to place your version of the following line in your `~/.casa/startup.py` file so that this is
automatically done for each CASA session.

```python
execfile("/users/user/DataComb/DC_locals.py")
```

where the path should be the path to `DC_locals.py` on your machine.

## Benchmark

Some of these tests take a long time (many hours), so for the GMC skymodel-b we have a shortened
version (GMC-bench) that will run with fewer data and fewer iterations, just to validate the process
(choices of CASA, analysisUtils and astropy could play a role here). 


```python
    !cp DC_pars-GMC-bench.py DC_pars.py
    execfile("DC_script.py")
```


