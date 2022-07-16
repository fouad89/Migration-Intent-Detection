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

from arabert.preprocess import ArabertPreprocessor
from common import Common
from config import *
import pandas
from transformers import AutoTokenizer
from transformers.data.processors.utils import InputFeatures


class Classifier( Common ):
    text = []
    model_name = ""
    max_len = 0
    label_map = dict()
    target = None
    tokenizer = None
    preprocessor = None
    defaults = {
        "model_name": "aubmindlab/bert-base-arabertv02",
        "max-length": 256,
        "truncation": "longest_first",
    }

    def __init__( self, *args, **kwargs ):
        super( ).__init__( *args, **kwargs )
        try:
            self.tokenizer = AutoTokenizer.from_pretrained( self.config["model_name"] )
            self.preprocessor = ArabertPreprocessor( model_name = self.config["model_name"], keep_emojis = False )
        except Exception as error:
            self.log.error( error )

    def __len__( self ):
        len( self.text )

    def __getitem__( self, item ):
        if not self.tokenizer or not self.text:
            return None
        text = str( self.text[item] )
        text = " ".join( text.split() )
        input_ids = self.tokenizer.encode(
                text,
                add_special_tokens = True,
                max_length = self.config["max-length"],
                truncation = self.config["truncation"]
        )
        attention_mask = [1] * len(input_ids)
        # Zero-pad up to the sequence length.
        padding_length = self.config["max-length"] - len(input_ids)
        input_ids = input_ids + ([ self.tokenizer.pad_token_id]  * padding_length)
        attention_mask = attention_mask + ([0] * padding_length)
        return InputFeatures(input_ids = input_ids, attention_mask = attention_mask)

    def load_train_ds( self, file_name, data = "text", mapping = { 0: "NEG", 1: "POS" } ) -> object:
        if not self.preprocessor:
            self.log.warning( "We have no processor even if we have a file, so quitting." )
            return None
        path = os.path.join( BASE_DIR, "data", file_name )
        if os.path.exists( path ) and os.path.isfile( path ):
            try:
                df = pandas.read_csv( path, index_col = 0 )
                self.log.debug( df.head( ) )
                self.text = df[data].apply( lambda x: self.preprocessor.preprocess( x ) ).to_list( )
                self.label_map = list( mapping.values( ) )
                return self
            except Exception as error:
                self.log.error( error )
                return None
        else:
            self.log.error( f"File {path} does not exists or not readable." )
            return None
