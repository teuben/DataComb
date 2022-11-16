# Quick Start Guide

This guide will walk you through how to run the data combination
script on example data and how to quickly run the script in the
future.

The general overview of the steps to get combination images:

1. Set data and user specific parameters in `DC_pars.py`
2. Execute `DC_locals.py` - if it was not done via CASA's startup.py
3. Execute `DC_script.py`

## Preparation

Before following this guide, you should have already:

- Installed CASA 6
	- Ensure astropy is installed
- Installed analysisutils
- Downloaded any example data and know the path to the data
- Configured your local paths (see [Preparation.md](Preparation.md))

## Step 1: Set parameters in DC_pars.py

You need to have a `DC_pars.py` for the data combination script to run. For your own data
simply copy an example parameter file and edit. For this example, we will use `DC_pars_M100.py`.  

```bash
  cp DC_pars_M100.py DC_pars.py
```
Make sure that you have the M100 data in the correct directory and have set up your local directories correctly.

## (Optional) Step 2: Execute `DC_locals.py`

If you DID NOT put a reference to `DC_locals.py` in your `~/.casa/startup.py` file,
you need to execute `DC_locals.py` in your current CASA session (and you will have
to continue to do so each time you start a new CASA session to work with this data combination script) by 

```python
  execfile("DC_locals.py")
```

Q: do we need globals() here ?

## Step 3: Run `DC_script.py`

The last step is to run the scripts to do the data combination in CASA

```python
  execfile("DC_script.py")
```


## Other examples

Other example data and parameter files that we provide:

* M100 - the casaguide example
* GMC  - the skymodel (formerly called skymodel-b)
