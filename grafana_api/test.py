#!/usr/local/bin/python3

import argparse
from web_api import api_get, api_go
import logging
import json
import pprint

# Module level resources
logr = logging.getLogger( __name__ )
resources = {}


def get_args( params=None ):
    key = 'args'
    if key not in resources:
        constructor_args = {
            'formatter_class': argparse.RawDescriptionHelpFormatter,
            'description': 'Interact with grafana API.',
            'epilog': '''NETRC:
                Login credentials should be stored in ~/.netrc.
                Machine name should be hostname only.
                ''',
            }
        parser = argparse.ArgumentParser( **constructor_args )
        parser.add_argument( '-d', '--debug', action='store_true' )
        parser.add_argument( '-v', '--verbose', action='store_true' )
        # # output format = raw for web use
        # parser.add_argument( '-o', '--output_format',
        #     choices=['text', 'csv', 'raw' ],
        #     default='text',
        # )
        # parser.add_argument( '-n', '--num_weeks',
        #     type=int,
        #     default=4,
        #     help='Number of weeks to report (default: %(default)s)')
        args = parser.parse_args( params )
        resources[key] = args
    return resources[key]


def get_warnings():
    key = 'errs'
    if key not in resources:
        resources[key] = []
    return resources[key]


def warn( msg ):
    ''' Log an warning to the screen and,
        Also save it in an array for later retrieval of all warnings.
    '''
    key = 'errs'
    if key not in resources:
        resources[key] = []
    resources[key].append( msg )
    logging.warning( msg )


def get_errors():
    key = 'errs'
    if key not in resources:
        resources[key] = []
    return resources[key]


def err( msg ):
    ''' Log an error to the screen and,
        Also save it in an array for later retrieval of all errors.
    '''
    key = 'errs'
    if key not in resources:
        resources[key] = []
    resources[key].append( msg )
    logging.error( msg )


def run():
    # Simple connect test using dashboard search api
    # path = 'search'
    # r = api_get( path )
    # pprint.pprint( r.json() )

    # Get folders
    # path = 'folders'
    # r = api_get( path, version='' )
    # # pprint.pprint( r.json() )
    # folders = {}
    # for folder in r.json():
    #     title = folder['title']
    #     folders[title] = folder

    # Get alerts
    path = 'provisioning/alert-rules'
    r = api_get( path )
    # pprint.pprint( r.json() )
    # f_uid = folders['ASD']['uid']
    for alert in r.json():
        # if alert['folderUID'] == f_uid:
        #     pprint.pprint( alert['title'] )
        # pprint.pprint( alert['title'] )
        title = alert['title']
        if title.startswith( '[ASD] ' ):
            print( f'--- {title} ---' )
            pprint.pprint( alert )

    
if __name__ == "__main__":
    args = get_args()

    # configure logging
    loglvl = logging.WARNING
    if args.verbose:
        loglvl = logging.INFO
    if args.debug:
        loglvl = logging.DEBUG
    logr.setLevel( loglvl )
    logfmt = logging.Formatter( '%(levelname)s:%(funcName)s[%(lineno)d] %(message)s' )
    ch = logging.StreamHandler()
    ch.setFormatter( logfmt )
    logr.addHandler( ch )

    # start processing
    run()

