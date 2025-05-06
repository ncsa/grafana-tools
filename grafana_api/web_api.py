import configparser
import logging
import netrc
import os
import pprint
import requests
# import requests.exceptions

from http.client import HTTPConnection
HTTPConnection.debuglevel = 1

# Module level resources
logr = logging.getLogger( __name__ )
resources = {}


def get_session():
    key = 'session'
    if key not in resources:
        resources[key] = requests.Session()
    return resources[key]


def get_config():
    key = 'cfg'
    if key not in resources:
        env_name = 'GRAFANA_API_CONFIG'
        conf_files = [
            './conf/config.ini',
            '~/.config/grafana-tools/config.ini',
            ]
        env_file = os.getenv( env_name )
        if env_file:
            conf_files.append( env_file )
        cfg = configparser.ConfigParser( allow_no_value=True )
        cfg.optionxform = str
        cfg.read( conf_files )
        resources[key] = cfg
    return resources[key]


def get_server_info():
    key = 'server_info'
    if key not in resources:
        config = get_config()
        server = config['server']
        resources[key] = server
        resources['server'] = server['host']
        resources['port'] = server['port']
        resources['scheme'] = server['scheme']
    return resources[key]


def get_server():
    key = 'server'
    if key not in resources:
        get_server_info()
    return resources[key]


def get_scheme():
    key = 'scheme'
    if key not in resources:
        get_server_info()
    return resources[key]


def get_port():
    key = 'port'
    if key not in resources:
        get_server_info()
    return resources[key]



def get_netrc():
    key = 'netrc'
    if key not in resources:
        n = netrc.netrc()
        server = get_server()
        (login, account, password) = n.authenticators( server )
        resources['login'] = login
        resources['account'] = account
        resources['password'] = password
        resources[key] = n
    return resources[key]


def get_login():
    key = 'login'
    if key not in resources:
        get_netrc()
    return resources[key]


def get_account():
    key = 'account'
    if key not in resources:
        get_netrc()
    return resources[key]


def get_password():
    key = 'password'
    if key not in resources:
        get_netrc()
    return resources[key]


def api_go( method, path, version='v1', **kw ):
    # srv_info = get_server()
    scheme = get_scheme()
    server = get_server()
    port = get_port()
    url = f'{scheme}://{server}:{port}/api/{version}/{path}'
    logr.debug( f'{method} {path}, {pprint.pformat(kw)}' )
    s = get_session()
    # to use personal access token, must disable netrc function in requests
    s.trust_env = False
    token = get_account()
    s.headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        }
    r = s.request( method, url, **kw )
    logr.debug( f'RETURN CODE .. {r}' )
    # llogr.debug( f'RETURN HEADERS .. {r.headers}' )
    r.raise_for_status()
    return r


def api_get( path, params=None, **kw ):
    return api_go( 'GET', path, params=params, **kw )


def api_delete( path, data=None ):
    kwargs = { 'timeout': 1800 }
    if data:
        kwargs.update ( { 'json': data } )
    return api_go( 'DELETE', path, **kwargs )


def api_post( path, data):
    return api_go( 'POST', path, json=data )


def api_put( path, data ):
    return api_go( 'PUT', path, json=data )


if __name__ == '__main__':
    raise UserWarning( 'Not directly runnable' )
