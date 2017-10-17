def set_cors_headers(headers):
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Headers'] = \
        'Origin, X-Requested-With, Content-Type, Accept, Key, Authorization '
    headers['Access-Control-Allow-Credentials'] = 'true'
    headers['Access-Control-Expose-Headers'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT'

