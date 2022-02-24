from django.shortcuts import render
from .log_file_processor import copy_log_file, filter_log, time_filtered_info
from datetime import datetime


def index(request):
    refresh_time = 1
    if request.POST:
        refresh_time = request.POST['refresh_time_name']
    copy_log_file
    filtered_log = filter_log()
    filtered_list = time_filtered_info(filtered_log)
    print(len(filtered_list))
    print(datetime.now())
    context = {
        'list': filtered_list,
        'refresh_time': int(refresh_time)*60,
    }
    return render(request, 'queue_checker/index.html', context)
