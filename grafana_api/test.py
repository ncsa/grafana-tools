#!/usr/local/bin/python3

import web_api
import logging

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


def run():
    pass
    

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
