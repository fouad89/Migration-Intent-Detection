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

from config import LOG_LEVEL
import logging


class Common:
    log = None
    level = LOG_LEVEL
    config = None
    defaults = dict( )

    def __init__( self, *args, **kwargs ):
        super( ).__init__( )
        self.log = logging.getLogger( self.__class__.__name__ )
        self.log.setLevel( kwargs["level"] if "level" in kwargs else LOG_LEVEL )
        if "config" in kwargs and isinstance( kwargs["config"], dict ):
            self.config = { **self.defaults, **kwargs["config"] }
        else:
            self.config = self.defaults

