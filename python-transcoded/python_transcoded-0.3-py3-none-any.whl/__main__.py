import configparser
import json
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
import os
import logging
import queue
import time
import shutil
from transcoded.log import logger
from transcoded.job import TranscodingJob
from transcoded.profile import Profile
import threading

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.disabled = False

jobs = queue.Queue()


def jobs_index(request):
    global jobs
    console = '*/*' in request.accept_mimetypes
    if console:
        result = ""
        for job in jobs.queue:
            result += repr(job) + "\n"
        return Response(result, status=200, content_type='text/plain')
    else:
        result = json.dumps(jobs)
        return Response(result, status=200, content_type='application/json')


def _check_path_permissions(path, username):
    for prefix in permissions[username]['paths']:
        if path.startswith(prefix):
            return True
    return False


def job_create(request, username):
    global jobs
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        logger.error('Received invalid response')
        return Response('No valid json data received', status=400)

    required = ['source', 'destination', 'profile']
    for field in required:
        if field not in data:
            return Response('Missing required field "{}"'.format(field), status=400)

    source = os.path.abspath(data['source'])
    destination = os.path.abspath(data['destination'])

    if not _check_path_permissions(source, username):
        return Response('Source path not allowed for {}'.format(username), status=403)
    if not _check_path_permissions(destination, username):
        return Response('Destination path not allowed for {}'.format(username), status=403)

    if data['profile'] not in profiles:
        return Response('Profile "{}" is not defined'.format(data['profile']), status=404)

    if not os.path.isfile(source):
        return Response('Source file does not exist', status=404)

    job = TranscodingJob()
    job.sources.append(data['source'])
    job.destination = data['destination']
    job.profile = profiles[data['profile']]
    job.user = username
    job.callback = permissions[username]['callback']
    if 'id' in data:
        job.foreign_id = data['id']
    jobs.put(job)
    return Response('Job is queued')


@Request.application
def application(request):
    if request.authorization is None:
        logger.warning('API Request without authentication received')
        return Response('Authorisation required', status=401, headers={'WWW-Authenticate': 'Basic realm="transcoded"'})
    username = request.authorization.username
    password = request.authorization.password
    if username not in permissions:
        logger.warning('User "{}" does not exist'.format(username))
        return Response('User "{}" does not exist'.format(username), status=401,
                        headers={'WWW-Authenticate': 'Basic realm="transcoded"'})
    if password != permissions[username]['password']:
        logger.warning('Incorrect password for user "{}"'.format(username))
        return Response('Login incorrect'.format(username), status=401,
                        headers={'WWW-Authenticate': 'Basic realm="transcoded"'})

    try:
        if request.path == '/jobs':
            if request.method == 'GET':
                return jobs_index(request)
            elif request.method == 'POST':
                return job_create(request, username)
    except Exception as e:
        logger.error(e)

    return Response('Endpoint does not exist', status=404)


def transcode_thread():
    while True:
        item = jobs.get()
        if item is None:
            time.sleep(5)
            continue

        item.run()


def parse_permissions(config):
    result = {}
    for section in config.sections():
        if section.startswith('user-'):
            username = section[5:]

            password = config.get(section, 'password', fallback=None)
            if password is None:
                logger.fatal("User '{}' has no password defined, exiting...".format(username))
                exit(1)

            raw_paths = config.get(section, 'paths', fallback='/')

            if raw_paths.strip().startswith('['):
                paths = json.loads(raw_paths)
            else:
                paths = [raw_paths]

            callback = config.get(section, 'callback', fallback=None)

            result[username] = {
                'username': username,
                'password': config.get(section, 'password'),
                'paths': paths,
                'callback': callback
            }
            logger.info('Added user {} from config'.format(username))
    return result


def parse_profiles(config):
    result = {}
    for section in config.sections():
        if section.startswith('profile-'):
            name = section[8:]
            result[name] = Profile(name, dict(config.items(section)))
            logger.info('Added profile {}'.format(result[name]))
    return result


def sanity_checks():
    if shutil.which('ffmpeg') is None and shutil.which('avconv') is None:
        print('Neither ffmpeg or avconv is installed')
        exit(1)

    if shutil.which('ffprobe') is None and shutil.which('avprobe') is None:
        print('Could not find ffprobe or avprobe')
        exit(1)


def main():
    global permissions, profiles
    import argparse

    sanity_checks()

    parser = argparse.ArgumentParser(description="Transcode daemon")
    parser.add_argument('--config', '-c', help="Config file location", default='/etc/transcoded.ini', type=str)
    args = parser.parse_args()

    logger.info('Starting transcode daemon')
    if not os.path.isfile(args.config):
        logger.fatal("Config file '{}' not found".format(args.config))
        exit(1)

    config = configparser.ConfigParser()
    try:
        config.read(args.config)
    except configparser.ParsingError as e:
        logger.fatal(e.message)
        exit(1)
    permissions = parse_permissions(config)
    profiles = parse_profiles(config)

    logger.info('Starting transcoding thread')
    thread = threading.Thread(target=transcode_thread)
    thread.daemon = True
    thread.start()

    logger.info('Starting http server on {}:{}'.format(config.get('general', 'listen'), config.get('general', 'port')))
    run_simple(config.get('general', 'listen'), int(config.get('general', 'port')), application)


if __name__ == '__main__':
    main()
