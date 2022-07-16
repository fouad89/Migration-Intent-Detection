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

import arabic_reshaper as ar
from bidi.algorithm import get_display
from datetime import datetime
import pandas
import time
import tweepy

from config import *
from common import Common

TWITTER_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Twitter( Common ):
    _client = None
    _words = []
    defaults = {
        "start_at": datetime.fromisoformat( "2010-01-01T00:00:00" ),
        "stop_at": datetime.fromisoformat( "2020-01-01T00:00:00" ),
        "country": "TN",
        "lang": "ar",
        "keyword-file": os.path.join( os.path.dirname( __file__ ), "01-seed_words.txt" ),
        "max-results": 500,
        "time-interval": 1,
    }
    tweets = None

    def __init__( self, token: str, *args, **kwargs ):
        super( ).__init__( *args, **kwargs )
        if token:
            try:
                self._client = tweepy.Client( token, wait_on_rate_limit = True )
            except Exception as err:
                self.log.error( err )
        self.log.debug( self.config )

    def keywords( self, file = None ):
        text_file = file or self.config["keyword-file"]
        with open( text_file, "r", encoding = "utf8" ) as f:
            self._words = f.read( ).splitlines( )
        return True

    def display_words( self ):
        return [ get_display( ar.reshape( t ) ) for t in self._words ]

    def query( self, keywords = None, start_at = None, stop_at = None, country = None, lang = 'ar' ):
        if self._client is None:
            self.log.warning( "Client is empty, so it will not query anything")
            return None
        if keywords is None:
            self.keywords( )
        config = {
            "keywords": keywords or self._words,
            "start_at": start_at or self.config["start_at"].strftime( TWITTER_TIME_FORMAT ),
            "stop_at": stop_at or self.config["stop_at"].strftime( TWITTER_TIME_FORMAT ),
            "country": country or self.config["country"],
            "lang": lang or self.config["lang"],
        }
        fields = [ "created_at", "geo", "public_metrics", "text", ]
        self.log.debug( config )
        tweets = [ r for word in config["keywords"] for r in tweepy.Paginator( self._client.search_all_tweets,
                query = f"{word} lang:{config['lang']} place_country:{config['country']}",
                tweet_fields = fields,
                start_time = config["start_at"],
                end_time = config["stop_at"],
                expansions = [ "geo.place_id", "author_id", ],
                next_token = {},
                max_results = self.config["max-results"] ) if time.sleep( self.config["time-interval"] ) or True ]
        self.tweets = tweets
        return True

    def save( self, output = None ):
        if self.tweets:
            data = [ { "tweet_id": t.id, "created_at": t.created_at, "text": t.text } for tw in self.tweets for t in tw.data if tw.data  ]
            df = pandas.DataFrame.from_records( data )
            outfile = output or f"{self.config['country']}_{self.config['lang']}_{self.config['start_at'].strftime('%Y%m%d')}_{self.config['stop_at'].strftime('%Y%m%d')}.csv"
            self.log.debug( df.head( ) )
            df.to_csv( os.path.join( BASE_DIR, "data", outfile ), encoding = "utf-8" )
            return df
        return None
