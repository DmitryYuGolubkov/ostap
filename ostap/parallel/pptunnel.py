#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
## @file ostap/parallel/pptunnel.py
#  Useful utilities for multiprocessing and parallel processing for Ostap
#  @author Vanya BELYAEV Ivan.Belyaev@itep.ru
#  @date   2016-02-23
# =============================================================================
"""Useful utilities for multiprocessing and parallel processing for Ostap
- Helper class to start remote ppserver (for parallel python)
"""
# =============================================================================
__version__ = '$Revision$'
__author__  = 'Vanya BELYAEV Ivan.Belyaev@itep.ru'
__date__    = '2016-02-23'
__all__     = (
    'ppServer' , ## helper class to start remote ppserver (for parallel python)
    )
# =============================================================================
from ostap.logger.logger import getLogger
if '__main__' == __name__ : logger = getLogger ( 'ostap.paralllel.pptunnel' )
else                      : logger = getLogger ( __name__                   ) 
# =============================================================================
import sys, os
import pathos.core    as PC
import pathos.secure  as PS
# =============================================================================
## @class ppServer
#  Helper class that starts <code>ppserver</code> on remote site
#  and makes SSH tunnel
#  @attention Password-less SSH-connection is required!
#  @code
#  pps = ppServer('lxplus009.cern.ch')
#  print pps.local, pps.remote
#  del pps
#  @endcode
#  ... or as context manager :
#  @code
#  with ppServer('lxplus009.cern.ch') as pps : 
#      print pps.local, pps.remote
#      ... do something here 
#  @endcode
#  @author Vanya BELYAEV Ivan.Belyaev@itep.ru
class ppServer(object) :
    """ Helper class that starts ppserver on remote site and makes SSH tunnel
    - attention:  password-less SSH-connection is required!
    
    >>> pps = ppServer('lxplus009.cern.ch')
    >>> print pps.local, pps.remote
    >>> del pps
    
    ... or as context manager :

    >>> with ppServer('lxplus009.cern.ch') as pps : 
    ...  print pps.local, pps.remote
    ...  do something here 
    """
    def __init__ ( self               ,
                   remote             ,
                   environment = ''   ,
                   script      = None ,
                   profile     = None ,
                   secret      = None ,
                   timeout     =   -1 ,
                   silent      = True ) :

        self.__session = None
        self.__pid     = 0
        
        ## split user@remote
        remote_user , at , remote = remote.rpartition('@')
        
        import socket        
        remote = socket.getfqdn ( remote ).lower()  

        ## ## merge user@remote 
        ## if remote_user and at : 
        ##     import getpass
        ##     local_user = getpass.getuser()
        ##     if remote_user.lower() != local_user.lower() :
        ##         remote = ''.join ( ( remote_user, at , remote ) )
                
        remote = ''.join ( ( remote_user, at , remote ) )
                
        self.__remote_host = remote 
        
        ## SSH tunnel 
        self.__tunnel       = PS.Tunnel  ( 'SSH-tunnel %s' %  self.remote_host  )
        self.tunnel.connect ( self.remote_host )

        logger.debug ('Create SSH tunnel: %s' %  self.tunnel )
            
        self.__local_port   = self.tunnel._lport 
        self.__remote_port  = self.tunnel._rport 
                                  
        ## SSH session
        self.__session      = PS.Pipe ( 'SSH-session' , host = self.remote_host )  

        logger.debug ('Create SSH session: %s'%  self.session )
        
        import logging
        verbose = logging.root.manager.disable <= logging.DEBUG 
        self.session.verbose = verbose
        self.tunnel .verbose = verbose 
        del logging

        # ==================================================================
        # Get configuration information for the given remote host
        if ( not environment ) or ( not script ) or ( not profile ) :
            from ostap.parallel.utils import get_remote_conf 
            e , s , p = get_remote_conf ( remote ) 
            if e and not environment : environment = e
            if s and not script      : script      = s
            if p and not profile     : profile     = p 

        if script :
            if os.path.exists ( script ) and os.path.isfile ( script ) : pass
            else :
                logger.error ("The script %s does not exist, skip it!" % script )
                script = None 
                                  
        ## temporary directory on remote host 
        self.__tmpdir = None 
        if environment or script or profile : 
            self.session  ( command =  'mktemp -d -t pathos-$(date +%Y-%b-%d)-XXXXXXXXX' )
            self.session.launch()
            r = self.session.response()
            if r and 1 < len ( r ) : 
                self.__tmpdir = r [:-1] 
                logger.verbose ('Created remote temporary directory %s:%s' % ( self.remote_host , self.__tmpdir ) ) 
            else :
                logger.error   ('Cannot create remote temporary directory at %s' % self.remote_host ) 
                
        self.__environment = None
        if  environment :
            import ostap.utils.cleanup as CU
            tmpfile = CU.CleanUp.tempfile ( prefix = 'env-' , suffix = '.sh' )
            with open ( tmpfile , 'w' ) as tf :
                tf.write( environment )
                tf.write('\n')
            copier      = PS.Copier ( 'SSH-copier' )
            destination = "%s:%s" % ( self.__remote_host , self.__tmpdir )
            copier ( source = tmpfile , destination = destination )
            copier.launch()
            r = copier.response()
            if r : logger.error ('SCP: response from %s : %s' % ( copier , r ) ) 
            del copier
            self.__environment = os.path.join ( self.__tmpdir , os.path.basename ( tmpfile ) )
            logger.verbose ('SCP: environment %s:%s is copied' % ( self.remote_host , self.__environment ) )
            
        self.__script = None 
        if  script and os.path.exists ( script ) and os.path.isfile ( script ) :
            copier      = PS.Copier ( 'SSH-copier' )
            destination = "%s:%s" % ( self.__remote_host , self.__remote_tmpdir )
            copier( source = script , destination = destination )
            copier.launch()
            r =  copier.response()
            if r : logger.error ('SPC: response from %s : %s' % ( copier , r ) ) 
            del copier
            self.__script = os.path.join ( self.__tmpdir , os.path.basename ( script ) )
            logger.verbose ('SCP: script      %s:%s is copied' %  ( self.remote_host , self.__script ) )
                

        self.__profile = None 
        if profile :
            self.session  ( command =  '[ -f %s ] && echo "1" || echo "0" ' %  profile  )
            self.session.launch()
            r = self.session.response()
            try :
                if int ( r ) : self.__profile = profile
            except :
                pass
            if self.__profile :
                logger.verbose ("Profile %s:%s is found"     %  ( self.remote_host , profile ) )
            else : 
                logger.warning ("Profile %s:%s is NOT found" %  ( self.remote_host , profile ) )

        commands = []
        if self.__profile     : commands.append ( ' source %s ' % profile            )
        if self.__environment : commands.append ( ' source %s ' % self.__environment )
        if self.__script      : commands.append ( ' source %s ' % self.__script      )
            
        ## pp-server itself:
        if   secret and 1 < timeout :
            commands.append ( 'ppserver -p %-7d -s %s -t %d'           % ( self.remote_port , secret , timeout ) )
            pattern = '[P,p]ython *.*ppserver *-p *%d *-s *%s *-t *%d' % ( self.remote_port , secret , timeout )
        elif secret :
            commands.append ( 'ppserver -p %-7d -s %s'                 % ( self.remote_port , secret ) ) 
            pattern = '[P,p]ython *.*ppserver *-p *%d *-s *%s'         % ( self.remote_port , secret )
        elif 1 < timeout : 
            commands.append ( 'ppserver -p %-7d -t %d'                 % ( self.remote_port , timeout ) ) 
            pattern = '[P,p]ython *.*ppserver *-p *%d *-t *%d'         % ( self.remote_port , timeout )
        else             : 
            commands.append ( 'ppserver -p %-7d'                       %   self.remote_port  ) 
            pattern = '[P,p]ython *.*ppserver *-p *%d'                 %   self.remote_port 

            
        command = ' && '.join ( commands ) 
        self.session ( command = command , background = True , options = '-f' ) 
        self.session.launch()
        r = self.session.response()
        if r : logger.error ('SERVER:response from %s : %s' % ( self.session , r ) )


        for i in range ( 15 ) :
            try :
                import time 
                time.sleep ( 1 )
                self.__pid = PC.getpid ( pattern , self.remote_host )
                logger.verbose ('PID for remote ppserver is %s:%d' % ( self.remote_host , self.__pid ) )
            except OSError : pass
            if self.__pid > 0 : break 
        else :
            logger.warning ('Cannot acquire PID for remote ppserver at %s:%s' % ( self.remote_host , self.remote_port ) )

        sys.stdout.flush () ## needed? 
        sys.stdin .flush () ## needed ?

        logger.debug   ( "%s" % self )
        logger.verbose ( command     )

        if not silent : 
            logger.info ( 'Tunnel: %6d -> %s:%s pid:%-6d' % ( self.local_port , self.remote_host , self.remote_port , self.pid ) )
            
    def start ( self ) : return self
    def end   ( self ) :

        sys.stdout.flush () ## needed ?
        sys.stdin .flush () ## needed ? 
        
        import logging
        verbose = logging.root.manager.disable <= logging.DEBUG 
        del logging
        
        if self.session : self.session.verbose = verbose 
        if self.tunnel  : self.tunnel .verbose = verbose 
        
        if self.__pid :
            try  :
                if self.session :  # and verbose :
                    command = 'kill -s SIGUSR1 %d ' % self.__pid 
                    self.session ( command = command )
                    self.session.launch   ()
                    r = self.session.response()
                    if r : logger.info ( '%s : %s : %s' %  ( self.remote_host , command , r ) )                    
                logger.debug ( 'Kill remote process %s:%s' % ( self.remote_host , self.__pid ) )
                PC.kill ( self.__pid , self.remote_host )
            except OSError :
                pass
        self.__pid = None

        ## remove unnesessary files 
        if self.session :
            commands = []
            if self.__environment : commands.append ( 'rm -f %s' %  self.__environment )
            if self.__script      : commands.append ( 'rm -f %s' %  self.__script      )
            if self.__tmpdir      : commands.append ( 'rmdir --ignore-fail-on-non-empty %s' %  self.__tmpdir ) 
            if commands :
                command = ' ; '.join ( commands )
                self.session ( command = command ) 
                self.session.launch()
                r = self.session.response () 
                if r : logger.verbose ( "Response: %s" % r )                
            
        if self.session :
            logger.debug ( 'Kill session      %s' % self.session ) 
            self.session.kill      () 

        if self.tunnel  :
            logger.debug ( 'Disconnect tunnel %s' % self.tunnel  ) 
            self.tunnel.disconnect ()

        self.__tunnel  = None
        self.__session = None

    ## CONTEXT MANAGER: empty
    def __enter__ ( self      ) : return self.start ()

    ## CONTEX MANAGER: exit 
    def __exit__  ( self, *_  ) : return self.end   () 

    ## delete, close and cleanup 
    def __del__   ( self )      :        self.end   ()

    # =========================================================================
    ## Readable printout: representation of ppServer/Tunnel
    #  @code
    #  s = ppServer ( ... )
    #  print(s)
    #  @endcode 
    def __repr__  ( self ) :
        """ Readable printout: Representation of ppServer/Tunnel
        >>> s = ppServer ( ... )
        >>> print(s) 
        """
        return "ppServer(%d:%s:%d,pid=%s)"  % ( self.local_port , self.remote_host , self.remote_port, self.pid )
    __str__ = __repr__
    
    @property
    def pid  ( self ) :
        """``pid''  : PID for remote ppserver process"""
        return self.__pid
    
    @property
    def script ( self ) :
        """``script'' : the shell script to be sourced to get the correct  environment"""
        return self.__script

    @property
    def environment ( self ) :
        """``environment'' : the environment script to be sourced to get the correct environment"""
        return self.__environment
    
    @property
    def remote_host      ( self ):
        """``remote_host'' : remote host"""
        return self.__remote_host

    @property
    def local_port  ( self ) :
        """``local_port'' : local port for SSH-tunnel"""
        return self.__local_port
    
    @property
    def remote_port ( self ) :
        """``remote_port'' : remote port for SSH-tunnel"""
        return self.__remote_port
        
    @property
    def tunnel   ( self ) :
        """``tunnel'' : SSH tunnel   local_port <---> remote_host:remote_port"""
        return self.__tunnel 
    
    @property
    def session ( self ) :
        """``tunnel'' : SSH session"""
        return self.__session 
    
    @property
    def local ( self ) :
        """``local'' : local server/tunnel address"""
        return "localhost:%s" % self.__local_port
    
    @property
    def remote ( self ) :
        """``remote'' : remote server/tunnel address"""
        return "%s:%s" % ( self.__remote_host , self.__remote_port )


# =============================================================================
if '__main__' == __name__ :
    
    from ostap.utils.docme import docme
    docme ( __name__ , logger = logger )
    
# =============================================================================
#                                                                       The END 
# =============================================================================