# -*- coding: utf-8 -*-
"""
#==========================================================================================
#
#    @title:         Implementation of run.py as Part of the Package ITFLOWS Arabic
#    @author:        fouad
#    @copyright:     MTU (all rights reserved)
#    @created:       2022. 07. 05.
#    @description:   Test and internal use only
#
#    @author abbreviations
#        fouad      = Fouad Shammary
#
#--------------------------------------------------------------------------------------
#    Modification    By          Changelog
#--------------------------------------------------------------------------------------
#    2022. 07. 05.     fouad       Initial version of run.py
#--------------------------------------------------------------------------------------
#
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
#==========================================================================================
"""
__author__ = "fouad"
__copyright__ = "MTU Cork, Bishoptown Campus, 2022, Project ITFLOWS"
__version__ = "0.01"
__status__ = "Production"
__date__ = "2022. 07. 05."

import json
import logging
import os

BASE_DIR = os.path.dirname( os.path.abspath( __file__ ) )
LOG_LEVEL = logging.INFO
ENV_VARIABLES = [ "CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET", "BEARER_TOKEN", ]

# -------------------------------------------------------------------------------------------------
#   Making loggers
# -------------------------------------------------------------------------------------------------
logging.basicConfig( level = LOG_LEVEL, format = "[%(levelname)s - %(asctime)s - %(name)s] >> %(filename)s %(lineno)s: %(message)s" )
log = logging.getLogger( "ITFLOWS" )

# -------------------------------------------------------------------------------------------------
#   Secrets are hidden, not part of this settings file
# -------------------------------------------------------------------------------------------------
CONFIG = { v: os.getenv( v ) for v in ENV_VARIABLES if os.getenv( v ) }
if len( CONFIG ) != len( ENV_VARIABLES ):
    with open( os.path.join( BASE_DIR, 'secret.json' ) ) as sensitive_file:
        try:
            CONFIG = { **json.load( sensitive_file ), **CONFIG }
        except Exception as err:
            log.warning( "Sensitive JSON file is malformed or inaccessible" )
            log.error( err )


