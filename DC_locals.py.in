# @EDIT_MSG@
#
# define setup parameters for our "scripts4paper" scripts and data
# also figure out if we're in python2 (CASA5) or python3 (CASA6)

_s4p      = '@S4P@/'        # the S4P scripts directory

_s4p_data = '@S4P_DATA@/'   # the S4P data directory, should be read only from here!
_s4p_work = '@S4P_WORK@/'   # the S4P work directory, you can write here!

# reuse them, but we should move to use the S4P variables
pathtoconcat = _s4p_data     # e.g. _s4p_data/skymodel-c.sim/skymodel-c_120L  is the root directory
pathtoimage  = _s4p_work


# why do we need two here ?
datacombpath = _s4p
TP2VISpath   = _s4p

import sys
sys.path.append(_s4p)


#  helper function for DC_script.py
def function_exists(fn):
    """
         fn (string) :  name of the function (or variable) to test if it exists
                        in your current python environment
    """
    #   surely there must be a better pythonic way for this?
    #   but this does work :-)
    try:
        a=eval('dir(%s)' % fn)
        print("Hurrah, %s exists" % fn)
        return True
    except:
        print("Warning: function %s not known" % fn)
        return False
    # should never get here
    return None


#  we can't work without the new sdintimaging....
if not function_exists('sdintimaging'):
    print('#########################################################')
    print('Your CASA version does not seem to  support sdintimaging.')
    print('Please use at least 6.1.x')
    print('Aborting script ...')
    print('#########################################################')
    sys.exit(1)


print("Setup of @S4P@ complete for python3 only")
print("S4P_DATA = @S4P_DATA@ (read only)")
print("S4P_WORK = @S4P_WORK@ (read/write)")
