#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) Ostap developers.
# ============================================================================= 
# @file test_fitting_pydf.py
# Test module for ostap/fitting/pypdf.py
# - It tests PyPDF construction
# ============================================================================= 
""" Test module for ostap/fitting/pypdf.py
- It tests ``pure-python'' PDF 
"""
# ============================================================================= 
from   __future__        import print_function
# ============================================================================= 
__author__ = "Ostap developers"
__all__    = () ## nothing to import
# ============================================================================= 
import ROOT, random, math
import ostap.fitting.roofit 
from   ostap.core.core      import VE, dsID, Ostap
from   ostap.fitting.basic  import MASS,     Fit1D 
from   ostap.fitting.pypdf  import PyPDF
from   builtins             import range
# =============================================================================
# logging 
# =============================================================================
from ostap.logger.logger import getLogger
if '__main__' == __name__  or '__builtin__' == __name__ : 
    logger = getLogger ( 'test_fitting_pypdf' )
else : 
    logger = getLogger ( __name__ )
# =============================================================================
## make simple test mass 
mass     = ROOT.RooRealVar ( 'test_mass' , 'Some test mass' , 3.0 , 3.2 )

## book very simple data set
varset0   = ROOT.RooArgSet  ( mass )
dataset   = ROOT.RooDataSet ( dsID() , 'Test Data set-0' , varset0 )  

mmin,mmax = mass.minmax()

## fill it 
m = VE(3.100,0.015**2)
for i in range(0,10000) :
    mass.value = m.gauss () 
    dataset.add ( varset0 )

logger.info ('DATASET %s' % dataset )

NORM = 1.0 / math.sqrt ( 2.0 * math.pi )
# =============================================================================
## @class PyGauss
#  local ``pure-python'' PDF 
class PyGauss(MASS,PyPDF) :
    """Local ``pure-python'' PDF """    
    def __init__ ( self         ,
                   name         ,
                   xvar         ,
                   mean  = ( 3.080 , 3.05  , 3.15  ) ,
                   sigma = ( 0.010 , 0.005 , 0.020 ) ,
                   pdf   = None ) :
        
        MASS .__init__ ( self , name      , xvar , mean , sigma ) 
        PyPDF.__init__ ( self , self.name , ( self.xvar  ,
                                              self.mean  ,
                                              self.sigma ) , pdf = pdf )
        self.config = {
            'name'  : self.name ,
            'xvar'  : self.xvar ,
            'mean'  : self.mean ,
            'sigma' : self.mean ,
            'pdf'   : None        ## attention! 
            }
        
    ## the  main method 
    def evaluate ( self ) :
        vlist = self.varlist

        x = float ( vlist [ 0 ] ) 
        m = float ( vlist [ 1 ] ) 
        s = float ( vlist [ 2 ] )        
        dx = ( x - m ) / s        
        return math.exp ( -0.5 * dx * dx ) * NORM / s 

CDF  = Ostap.Math.gauss_cdf
# =============================================================================
## @class PyGaussAI
#  local ``pure-python'' PDF with analytical integrals 
class PyGaussAI(PyGauss) :
    """Local ``pure-python'' PDF with analytical integrals """    
    def __init__ ( self         ,
                   name         ,
                   xvar         ,
                   mean  = (         3.05  , 5.15  ) ,
                   sigma = ( 0.010 , 0.005 , 0.025 ) ,
                   pdf   = None ) :

        PyGauss.__init__ (  self , name , xvar , mean , sigma , pdf = pdf )

        a =  QUQU


    ## declare analytical integral 
    def get_analytical_integral ( self ) :
        """Declare the analytical integral"""
        
        x  = self.varlist[0]
        
        if self.matchArgs ( x ) : return 1 ## get the integration code
        
        return 0
    
    ## calculate the analytical integral 
    def analytical_integral ( self ) :
        """Calculate the analytical integral"""

        assert 1 == self.intCode , 'Invalid integration code!'
        
        vlist = self.varlist

        rn    = self.rangeName        
        xv    = vlist [ 0 ]        
        xmax  = xv.getMax ( rn )
        xmin  = xv.getMin ( rn )
        
        m     = float ( vlist [ 1 ] ) 
        s     = float ( vlist [ 2 ] )        
        
        return CDF ( xmax , m , s  ) - CDF ( xmin , m , s  )
    
# =============================================================================
## pygauss PDF
# =============================================================================
def test_pygauss() :
    
    logger.info ('Test PyGauss:  simple Gaussian signal' )
    
    gauss   = PyGauss( 'PyGauss'   , xvar = mass )
    
    r1, f1  = gauss  .fitTo ( dataset , draw = True , silent = True , ncpu=1 )
    print (r1) 


# =============================================================================
## pygauss PDF
# =============================================================================
def test_pygauss_AI() :
    
    logger.info ('Test PyGaussAI:  simple Gaussian signal with  analytical integral' )
    
    gaussAI = PyGauss( 'PyGaussAI' , xvar = mass )
    r2, f2  = gaussAI.fitTo ( dataset , draw = True , silent = True , ncpu=1 )
    print(r2)

# =============================================================================
if '__main__' == __name__ :

    test_pygauss          () ## simple Gaussian PDF
    test_pygauss_AI       () ## simple Gaussian PDF with analytical integral 

# =============================================================================
# The END 
# ============================================================================= 