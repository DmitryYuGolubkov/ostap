#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# =============================================================================
## @file
#  Format the list of rows as a  table.
#  When <code>terminaltables</code> module is accessible,
#  use it to get nice pretty tables, otherwise use some home-made primitives
#  @see https://pypi.org/project/terminaltables
#  @see https://github.com/Robpol86/terminaltables
# 
#  @author Vanya BELYAEV Ivan.Belyaev@itep.ru
#  @date   2019-08-30
# =============================================================================
""" Format the list of rows as a table.
When terminaltables module is accessible,
use it to get nice pretty tables, otherwise use some home-made primitives
- see https://pypi.org/project/terminaltables
- see https://github.com/Robpol86/terminaltables
""" 
# =============================================================================
__version__ = "$Revision$"
__author__  = "Vanya BELYAEV Ivan.Belyaev@itep.ru"
__date__    = "2019-08-31"
__all__     = (
    'table'        , ## format the list of rows as a  table.
    'the_table'    , ## format the list of rows as a  table (local version)
    'table_width'  , ## true  width of the table
    'align_column' , ## align the certain column of the table  
    'add_prefix'   , ## add the prefix to each row of the table 
    )
# =============================================================================
import textwrap 
from   ostap.logger.colorized import infostr, allright, decolorize        
from   ostap.utils.basic      import terminal_size 
# =============================================================================
try :
    import terminaltables
except ImportError :
    terminaltables = None
# =============================================================================
left        = '<' , 'l' , 'left'  
right       = '>' , 'r' , 'right' 
center      = '^' , 'c' , 'center' , '='
wrapped     = 'w' ,
max_width   = 50
wrap_indent = '  '
# =============================================================================
## Format the list of rows as a  table (home-made primitive) 
#  - Each row is a sequence of column cells.
#  - The first row defines the column headers.
#  @code
#  table_data = [
#     ( 'Name'  , 'Occupation' , 'Note' ) ,
#     ( 'Alice' , '?'          , '---'  ) ,
#     ( 'Bob'   , 'unemployed' , ''     ) ,
#     ]
#  t = the_table ( table_data , 'Title' )
#  print (t)
#  @endcode
def the_table ( rows , title = '' , prefix = '' , alignment = () , wrap_width = -1 , indent = wrap_indent ) :
    """Format the list of rows as a  table (home-made primitive) 
    - Each row is a sequence of column cells.
    - The first row defines the column headers.
    >>> table_data = [
    ...   ( 'Name'  , 'Occupation' , 'Note' ) ,
    ...   ( 'Alice' , '?'          , '---'  ) ,
    ...   ( 'Bob'   , 'unemployed' , ''     ) ]
    >>> t = the_table ( table_data , 'Title' )
    >>> print (t)
    """
    ## calculate the number of columns

    rows = list ( rows )
    
    nc  = 0
    for row in rows : nc = max ( nc , len ( row ) )

    wraps = [] 
    for i , a in  zip ( range ( nc ) , alignment ) :
        if a and isinstance ( a , str ) :
            al = a.lower() 
            if   al in left  : pass 
            elif al in right : pass 
            elif al in wrapped : wraps.append ( i ) 

    ## calculate the maximum width for columns 
    widths = {}
    for k , row in enumerate ( rows ) :
        cols = [ c for  c in row ]
        while len  ( cols ) < nc : cols.append ('')             
        for i , c in enumerate ( cols ) :
            if not i in widths : widths[i] = 1
            widths [ i ] = max ( widths[i] , len ( decolorize ( c ) ) )
        cols = tuple ( cols )
        rows [ k ] = cols 

    ## play with wrapped columns
    while  wraps :

        twidth = 1 + len ( prefix )
        
        for k in widths :
            if not k in wraps :
                twidth += widths [ k ] + 2
                twidth += nc + 1                
        _ , w = terminal_size()
        if w <= twidth : break
        
        nw = len ( wraps ) 
        ww = ( w - twidth ) - 2 * nw
        ww , _ = divmod ( ww  , nw )

        if 12 < wrap_width and wrap_width < ww :
            ww = wrap_width
            
        if ww < 15 : break

        lw = len ( wraps )                 
        wraps = [ i for i in wraps if ww <= widths [i] ]
        
        if len ( wraps ) == lw  : break 

        
    for i in wraps :
        widths [ i ] = min ( ww  , widths [ i ] ) 

            
    hformats = [  "{:^%d}"  % widths [ c ] for c in range ( nc ) ]
    rformats = [ " {:^%d} " % widths [ c ] for c in range ( nc ) ]

    for i , a in  zip ( range ( nc ) , alignment ) :
        if a and isinstance ( a , str ) :
            al = a.lower() 
            if   al in left  or al in wrapped :
                hformats [ i ] = hformats [ i ].replace ( '^' , '<' )
                rformats [ i ] = rformats [ i ].replace ( '^' , '<' )
            elif al in right :
                hformats [ i ] = hformats [ i ].replace ( '^' , '>' )
                rformats [ i ] = rformats [ i ].replace ( '^' , '>' )

    if wraps :
        rows_ = rows
        rows  = [] 
        for row in rows_ :
            cells = [] 
            for i , c in enumerate ( row ) :
                if i in wraps and wrap_width < len ( c ) : cells.append ( textwrap.wrap ( indent + c , widths [ i ]  ) )
                else          : cells.append ( [ c ] )
            nr = 0 
            for c in cells : nr = max ( nr , len ( c ) )
            
            for l in cells :
                while len  (l )  < nr :
                    l.insert ( 0 , '' )
                    l.append (     '' )
                                        
            for r in range ( nr ) :
                new_row = [] 
                for i , c in enumerate ( cells ) :
                    lc = len ( c )
                    if r < lc : new_row.append ( c[r] )
                    else      : new_row.append ( ''   )
                rows.append ( new_row )
                
    totwidth = 0
    for c in widths : totwidth += widths[c]
    totwidth += ( nc - 1 ) * 3
    if totwidth < len ( title )  :
        delta = 1 + ( len ( title ) - totwidth ) // nc
        for c in widths : widths[c] += delta 

            
    seps     = [   '-' * ( widths [ c ]  + 2 ) for c in range ( nc ) ]
    sepline  = '+' + "+".join (  seps ) +  '+'

    table    = []
    if title :
        sline = '+' + '-' * ( len ( sepline ) - 2 ) + '+'
        tfmt  = "{:^%d}"  % ( len ( sepline ) - 4 )
        t     = '| ' + allright ( tfmt.format ( decolorize ( title ) ) ) + ' |'
        table.append ( sline  )
        table.append ( t      )

    table.append ( sepline )    
    for i , row in enumerate ( rows ) :
        
        cols = [ c for  c in row ]
        while len  ( cols ) < nc : cols.append ('')             

        if 0 == i :
            table.append ( '| ' + ' | '.join ( [ infostr ( f.format ( decolorize ( i ) ) )  for ( f , i ) in zip ( hformats , cols ) ] ) + ' |' ) 
            table.append ( sepline )             
        else :
            table.append ( '|'  +  '|' .join ( [           f.format ( decolorize ( i ) )    for ( f , i ) in zip ( rformats , cols ) ] ) +  '|' ) 

    table.append ( sepline )
    
    return prefix + ( '\n' + prefix ) .join ( table ) if prefix else '\n'.join ( table ) 

# =============================================================================
## Format the list of rows as a  table.
#  - Each row is a sequence of column cells.
#  - The first row defines the column headers.
# 
#  When <code>terminaltables</code> module is accessible,
#  use it to get nice pretty tables, otherwise use some
#  home-made primitive replacement 
#  @see https://pypi.org/project/terminaltables
#  @see https://github.com/Robpol86/terminaltables
#  @code
#  table_data = [
#     ( 'Name'  , 'Occupation' , 'Note' ) ,
#     ( 'Alice' , '?'          , '---'  ) ,
#     ( 'Bob'   , 'unemployed' , ''     ) ,
#     ]
#  t = table ( table_data , 'Title' )
#  print (t)
#  @endcode
def table ( rows , title = '' , prefix = '' , alignment = () , wrap_width = -1 , indent = wrap_indent  ) :
    """Format the list of rows as a  table.
    - Each row is a sequence of column cells.
    - The first row defines the column headers.

    When terminaltables package is accessible,
    use it to get nice pretty tables, otherwise use some
    home-made primitive replacement 
    - see https://pypi.org/project/terminaltables
    - see https://github.com/Robpol86/terminaltables

    >>> table_data = [
    ...   ( 'Name'  , 'Occupation' , 'Note' ) ,
    ...   ( 'Alice' , '?'          , '---'  ) ,
    ...   ( 'Bob'   , 'unemployed' , ''     ) ]
    >>> t = table ( table_data , 'Title' )
    >>> print (t)
    """
    
    from ostap.utils.basic import isatty

    title = allright ( decolorize ( title ) )
    if rows :
        rows       = list  ( rows ) 
        header_row = rows[0]
        header_row = [ infostr ( decolorize ( c ) ) for c in header_row ]
        rows [0]   = header_row 
        rows = tuple ( rows )
        
    rows = [ list(row) for row in rows ]

    if not terminaltables :
        
       ## use the local replacement 
        return the_table ( rows , title , prefix , alignment = alignment )


    if isatty () :
        
        title = allright ( title ) 
        table_instance = terminaltables.SingleTable ( rows , title )
        
    else :
        
        title = allright ( title ) 
        table_instance = terminaltables.AsciiTable ( rows , title)
        
    cw = table_instance.column_widths
    nc = len ( cw )

    wraps = [   i  for (i,a) in enumerate ( alignment ) if a in wrapped ]
    
    if wraps : 
        from terminaltables.width_and_alignment import max_dimensions
        widths = max_dimensions ( table_instance.table_data    ,
                                  table_instance.padding_left  ,
                                  table_instance.padding_right ) [2] 
        widths = sum ( l  for (i,l) in enumerate ( widths ) if not i in wraps ) 
        widths += nc + 1 + len ( prefix ) + 4 + 2 * len ( wraps )              
        _ , w = terminal_size()
        ww = w - widths
        ww , _ = divmod ( ww , len ( wraps ) )
        
        if   12 < ww and ww < wrap_width : wrap_width = ww
        elif 12 < ww and wrap_width <= 0 : wrap_width = ww
        
        if wrap_width < 12 : wrap_width = max_width 
    
    nw = len ( wraps ) 
            
    
    for i, a in zip ( range ( nc ) , alignment ) :
        if a and isinstance ( a , str ) :
            al = a.lower() 
            if   al in left   : table_instance.justify_columns [ i ] = 'left'
            elif al in right  : table_instance.justify_columns [ i ] = 'right'
            elif al in center : table_instance.justify_columns [ i ] = 'center'
            elif al in wrapped :
                maxw  = table_instance.column_max_width ( i )
                if 15 < wrap_width * nw < maxw : maxw = ( wrap_width - 3 ) * nw if 1 < nw else wrap_width 
                if maxw < 15 :                   maxw = ( wrap_width - 3 ) * nw if 1 < nw else wrap_width 
                if maxw < 15 :                   maxw = ( max_width  - 3 ) * nw if 1 < nw else max_width
                width = maxw / nw if 1 < nw else maxw 
                for l , line in enumerate ( table_instance.table_data ) :
                    if width < len ( line [ i ] ) : 
                        table_instance.table_data[l][i] = textwrap. fill ( indent + line [ i ] , wrap_width  )
                        
    return add_prefix ( table_instance.table , prefix ) 
    
# =============================================================================
## get the true  table width 
def table_width  ( table ) :
    """Get the true width of the table
    """
    width = 0
    for row in table.split('\n') :
        width = max ( width , len ( decolorize ( row ) ) )
    return width 

# =============================================================================
## Add certain prefix to  each line of the table
#  @code
#  table = ...
#  table =  add_prefix ( table , '# ') 
#  @endcode
def add_prefix ( table , prefix = '' ) :
    """Add certain prefix to  each line of the table
    >>> table = ...
    >>> table =  add_prefix ( table , '# ') 
    """
    return prefix + table.replace ( '\n' , '\n' + prefix ) if prefix else table 

# ==============================================================================
## Align the certain column of the table
#  @code
#  aligned = align_column ( table , 1 , 'left' ) 
#  @endcode 
def align_column ( table , index , align = 'left') :
    """Aling the certain column of the table
    >>> aligned = align_column ( table , 1 , 'left' ) 
    """
    nrows = [ list ( row ) for row in table ]
    lmax  =  0 

    for row in nrows :
        if index <= len ( row ) :
            item = decolorize ( row [ index ] )
            lmax = max ( lmax , len ( item )  )

    if not lmax : return table 

    aleft   =               align.lower() in left 
    aright  = not aleft and align.lower() in right 

    new_table = []
    for row in nrows :
        if index <= len ( row ) :
            item   = decolorize ( row [ index ] )
            nspace = lmax - len ( item ) 
            if   aleft :
                item = row [ index ] + nspace * ' '
            elif aright:
                item = nspace * ' ' + row [ index ]
            else :
                sl = nspace / 2
                sr = nspace - sl 
                item = sl * ' ' + row [ index ] + sr * ' '
            row[ index ] = item                        
        new_table.append ( row )
            
    return [ tuple ( row ) for row in new_table ] 
    
# =============================================================================
if __name__ == '__main__' :

    from ostap.logger.logger import getLogger
    logger = getLogger ( 'ostap.logger.table')

    from ostap.utils.docme import docme
    docme ( __name__ , logger = logger )
    
    if terminaltables :
        logger.info     ( "``terminaltables'' will be used for formatting" )
    else :
        logger.warning  ( "``terminaltables'' is not available, use local replacement" )
        
    table_data = [
        ( 'Name'  , 'Occupation' , 'Note' ) ,
        ( 'Alice' , '?'          , '---'  ) ,
        ( 'Bob'   , 'unemployed' , ''     ) ]
    
    logger.info ( 'The table is \n%s' % table     ( table_data , 'Title' , alignment = 'rrr' ) ) 
    logger.info ( 'The table is \n%s' % table     ( table_data , 'Title' , alignment = 'lll' ) ) 
    logger.info ( 'The table is \n%s' % table     ( table_data , 'Title' , alignment = 'ccc' ) ) 
    logger.info ( 'The table is \n%s' % the_table ( table_data , 'Title' , alignment = 'rrr' ) ) 
    logger.info ( 'The table is \n%s' % the_table ( table_data , 'Title' , alignment = 'lll' ) ) 
    logger.info ( 'The table is \n%s' % the_table ( table_data , 'Title' , alignment = 'ccc' ) ) 
    logger.info ( 'The table with prefix is \n%s' %
                  table     ( table_data , 'Title' , prefix = '# ' ) ) 
    logger.info ( 'The table with prefix is \n%s' %
                  the_table ( table_data , 'Title' , prefix = '# ' ) ) 
    
    
# =============================================================================
##                                                                      The END 
# =============================================================================
