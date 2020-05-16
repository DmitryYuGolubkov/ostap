#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) Ostap developers.
# ============================================================================= 
# @file test_fitting_transform.py
# Test module 
# - It tests transform-PDF  
# ============================================================================= 
""" Test module 
- It tests transform-PDF 
"""
# ============================================================================= 
__author__ = "Ostap developers"
__all__    = () ## nothing to import
# ============================================================================= 
import ROOT, random
import ostap.fitting.roofit
from   ostap.core.core             import cpp, VE, dsID
import ostap.fitting.models        as     Models
from   ostap.fitting.transform_pdf import TrPDF
from   ostap.fitting.funbasic      import Fun1D
from   builtins                    import range
# =============================================================================
# logging 
# =============================================================================
from ostap.logger.logger import getLogger
if '__main__' == __name__  or '__builtin__' == __name__ : 
    logger = getLogger ( 'test_fitting_transform' )
else : 
    logger = getLogger ( __name__ )
# =============================================================================


# =============================================================================
def  test_transform () :
    
    x  = ROOT.RooRealVar('x','',1,100000)
    mean  =  1000
    sigma =  1000 

    ## book very simple data set
    varset  = ROOT.RooArgSet  ( x  )
    dataset = ROOT.RooDataSet ( dsID() , 'Test Data set' , varset )  
    while len ( dataset ) < 5000 : 
        v = random.gauss ( mean , sigma )
        if v in x :
            x.value = v 
            dataset.add ( varset  )
            
    dataset.add_var ( 'lx' , 'log10(x)' ) 
    dataset.lx.setMin ( 0 ) 
    dataset.lx.setMax ( 5 )
    
    ## original PDF 
    g = Models.Gauss_pdf ( 'G' , xvar = x ,
                           mean  = ( mean  , mean  / 2 , mean  * 2 ) , 
                           sigma = ( sigma , sigma / 2 , sigma * 2 ) )
    
    
    r1 , f1  = g.fitTo  ( dataset , draw = True  , silent = True )
    logger.info ( 'Fit x:\%s' % r1.table() ) 

    if not 62000 <= ROOT.gROOT.GetVersionInt() :
        logger.warning("Not for tihs version of ROOT")
        return
    
    lx = dataset.lx
    LX = Fun1D (  lx , lx )
    NX = 10 ** LX
    
    ## transformed PDF 
    t  = TrPDF ( pdf = g , new_var = NX )
    
    r2 , f2 = t.fitTo  ( dataset , draw = True  , silent = True )
    logger.info ( 'Fit log10(x):\%s' % r2.table() ) 

    
# =============================================================================
if '__main__' == __name__ :

    test_transform    () 
    
# =============================================================================
##                                                                      The END 
# =============================================================================