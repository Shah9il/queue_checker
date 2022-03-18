import os
from django.shortcuts import render
from .log_file_processor import copy_log_file, filter_log, time_filtered_info, get_provider_data
import logging
from datetime import datetime
from dotenv import load_dotenv
import socket

load_dotenv()
logger = logging.getLogger(__name__)

hostname = socket.gethostname()

LINE_COUNT = os.getenv('LINE_COUNT')
DJANGO_ENV = os.getenv('DJANGO_ENV')


def index(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        logger.debug('Client IP: ' + request.environ['REMOTE_ADDR'])
    else:
        logger.debug('Client IP: ' + request.environ['HTTP_X_FORWARDED_FOR'])
    # ip_address = socket.gethostbyname(hostname)
    # logger.debug('Client IP: ' + ip_address)
    refresh_time = 1
    if request.POST:
        refresh_time = request.POST['refresh_time_name']
    logger.debug('Initiating file copy')
    # logger.debug(DJANGO_ENV)
    if DJANGO_ENV == 'LIVE':
        copy_log_file(LINE_COUNT)
    logger.debug('Initiating file read')
    filtered_log = filter_log()
    filtered_list = time_filtered_info(filtered_log)
    logger.debug(len(filtered_list))
    # logger.debug(filtered_list)
    unique_provider_ids = list(set([x[2] for x in filtered_list]))
    logger.debug(f'unique_provider_ids: {unique_provider_ids}')
    provider_data = get_provider_data(unique_provider_ids)
    for i in range(0, len(filtered_list)):
        # logger.debug(f'{filtered_list[i][0]}, {filtered_list[i][2]}')
        filtered_list[i][0] = provider_data[filtered_list[i][2]]
    f_list_web = [[x[0],x[1], x[3], x[4]] for x in filtered_list]
    logger.debug(datetime.now())
    context = {
        'list': f_list_web,
        'refresh_time': int(refresh_time)*60,
        'refresh_in_min': int(refresh_time),
        'provider_data': provider_data,
    }
    return render(request, 'queue_checker/index.html', context)
