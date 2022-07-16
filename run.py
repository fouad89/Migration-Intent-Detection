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

import argparse
from datetime import datetime
import sys

from config import *
from twitter import Twitter
from classifier import Classifier


def parse_argument( ):
    parser = argparse.ArgumentParser( )
    # sub_parser = parser.add_subparsers( title = "Valid sub-commands", description = """One can query and store Twitter data using environment variable or a config file.""" )
    sub_parser = parser.add_subparsers( title = "Valid sub-commands", dest = "command", required = True, description = """One can query and store Twitter data using environment variable or a config file.""" )
    #
    load = sub_parser.add_parser( 'load', help = "Load Twitter data for analysis" )
    load.add_argument( "-l", "--lang", dest = "language", default = 'ar', help = "Two letter Twitter language code." )
    load.add_argument( "-c", "--country", dest = "country", default = 'TN', help = "Two letter Twitter country code." )
    load.add_argument( "-f", "--from", dest = "start_at", default = '2010-01-01', help = "Starting date of interesting tweets starting with this date using data format: YYYY-MM-DD." )
    load.add_argument( "-u", "--until", dest = "end_at", default = '2020-01-01', help = "End of the time frame using date format: YYYY-MM-DD." )
    load.add_argument( "-m", "--max", dest = "max_result", type = int, default = 250, help = "Maximum samples to be downloaded by keyword elements (between 10 and 500)." )
    load.add_argument( "-k", "--keywords", dest = "keyword", help = "Seed word file to be used using a relative path to this file." )
    load.add_argument( "-w", "--wait", dest = "wait", type = int, help = "Time in seconds to be waited between each Twitter stream call." )
    #
    train = sub_parser.add_parser( 'train', help = "Trains a BERT model based on annotated file." )
    train.add_argument( "-d", "--data", dest = "file", required = True, default = "augmented_data.csv", help = "Annotated data to be used. It must be place at the data directory." )
    train.add_argument( "-f", "--field", dest = "field", default = "text", help = "Relevant column which contains the text to be processed." )
    train.add_argument( "-m", "--model", dest = "model", default = "aubmindlab/bert-base-arabertv02", help = "BERT model to use." )
    train.add_argument( "-l", "--max-length", dest = "max_len", type = int, default = 256, help = "Maximum length of input vector." )
    train.add_argument( "-t", "--truncation", dest = "trunc", default = "longest_first", help = "Truncation parameter of the model." )
    #
    help = sub_parser.add_parser( 'help', help = "Print this information" )
    # .add_argument_group( title = "Pre-train model", description = """It trains your model based on the input file given.""" )
    parser.print_help( )
    parser.print_usage( )
    #
    args = parser.parse_args( )
    return args


if __name__ == '__main__':
    log.debug( os.environ )
    try:
        args = parse_argument( )
        config = dict( )
        message = f"Using configuration for {args.command}"
        if args.command == "load":
            config = {
                "start_at": datetime.strptime( args.start_at or "2010-01-01", "%Y-%m-%d" ),
                "stop_at": datetime.strptime( args.end_at or "2025-01-01", "%Y-%m-%d" ),
                "country": args.country or "TN",
                "lang": args.language or "ar",
                "keyword-file": os.path.join( os.path.dirname( __file__ ), args.keyword or "01-seed_words.txt" ),
                "max-results": args.max_result if args.max_result and args.max_result >= 10 and args.max_result <= 500 else 500,
                "time-interval": args.wait or 1,
            }
            log.info( f"{message}:\n{config}" )
            twitter = Twitter( token = CONFIG["BEARER_TOKEN" ], config = config )
            # if twitter.query( ):
            #    twitter.save( )
        elif args.command == "train":
            config = {
                "model_name": args.model or "aubmindlab/bert-base-arabertv02",
                "max-length": args.max_len or 256,
                "truncation": args.trunc or "longest_first",
                "field": args.field or "text",
            }
            log.info( f"{message}:\n{config}" )
            classifier = Classifier( config = config )
            classifier.load_train_ds( file_name = args.file, data = config["field"] )
    except Exception as error:
        import traceback
        log.error( sys.exc_info() )
        traceback.print_exception( *(sys.exc_info()) )
    finally:
        pass
