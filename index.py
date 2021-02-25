# -*- coding: utf-8 -*-

import oss2
import subprocess
import os
import time
import ast
import shutil
import json

HELLO_WORLD = b'200 OK!\n'


# if you open the initializer feature, please implement the initializer function, as below:
# def initializer(context):
#    logger = logging.getLogger()  
#    logger.info('initializing')

def handler(environ, start_response):
    endpoint = '' # fill your oss endpoint
    bucketname = '' # fill your oss bucketname
    accessKeyId = '' # fill your oss accessKeyId
    accessKeySecret = '' # fill your oss accessKeySecret

    auth = oss2.Auth(accessKeyId, accessKeySecret)
    bucket = oss2.Bucket(auth, endpoint, bucketname)
    bucket.get_object_to_file('id_rsa', '/tmp/id_rsa')
    bucket.get_object_to_file('my_ssh_executable.sh', '/tmp/my_ssh_executable.sh')
    subprocess.Popen(['chmod 0600 /tmp/id_rsa'], shell=True)
    subprocess.Popen(['chmod +x /tmp/my_ssh_executable.sh'], shell=True)

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    print request_body
    request_body = json.loads(request_body)
    branch = request_body.get('ref').split('/')[-1]
    sshurl = request_body.get('repository').get('git_ssh_url')
    repositoryname = request_body.get('repository').get('name')
    password = request_body.get('password')
    print branch, sshurl, repositoryname
    
    localpath = '/tmp/{}'.format(repositoryname)
    if os.path.exists(localpath):
        shutil.rmtree(localpath)
    gitclone = 'GIT_SSH="/tmp/my_ssh_executable.sh" git clone -b {b} {u}'.format(b=branch, u=sshurl)
    subprocess.Popen([gitclone], shell=True, cwd='/tmp')
    time.sleep(5)

    # upload code to OSS
    rt = subprocess.Popen(['find {localpath} -type f ! -path "{localpath}/.git/*"'.format(localpath=localpath)],
                          shell=True, stdout=subprocess.PIPE)
    files = rt.stdout.readlines()
    for f in files:
        localfile = f.replace("\n", "")
        ossfile = localfile.replace(localpath, repositoryname + '/' + password, 1)
        print localfile, ossfile
        if os.path.isfile(localfile):
            bucket.put_object_from_file(ossfile, localfile)

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]
