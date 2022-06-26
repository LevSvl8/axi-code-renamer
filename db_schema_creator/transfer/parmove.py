import os
os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"

import datetime

from aconn import AConnector
from transfer.mxmovepar import copy_records, create_schema

import multiprocessing
import time
import json

def now():
    return datetime.datetime.now().strftime("%H:%M:%S")


def worker(tab_queue: multiprocessing.Queue, log_lock: multiprocessing.RLock,
           src_params, dest_params,
           src_model_tables, dest_model_tables,
           report_filename, journal_dir,
           packet_size=1000):

    my_name = multiprocessing.current_process().name
    task_no = 0

    def log(text):
        if task_no == 0:
            tx = '[%s$%s] %s' % (now(), my_name, text)
        else:
            tx = '[%s$%s#%s] %s' % (now(), my_name, task_no, text)

        log_lock.acquire()
        with open(report_filename, 'a', encoding='cp1251') as f:
#            f.write(tx + '\n')
            log_lock.release()
        print('\r' + tx + '                                        ')


    log('Connecting to databases')
    src = AConnector(my_name + '$' + src_params['name'], src_params['conn'], logger_fnc=log, encoding=src_params['encoding'],
                     schema_name=src_params['name'], echo=False)
    dest = AConnector(my_name + '$' + dest_params['name'], dest_params['conn'], logger_fnc=log,
                      schema_name=dest_params['name'], encoding=dest_params['encoding'], echo=False) #, convert_unicode=True
    # dest.engine.dialect.psycopg2_batch_mode = True
    paused = False
    while True:

        # check if stop file exists
        try:
            with open('worker', 'r') as f:
                text = f.read()
                if text == 'stop':
                    log('STOP command')
                    return
                elif text == 'pause':
                    if not paused:
                        log('PAUSE command')
                        paused = True
                    time.sleep(10)
                    continue
        except:
            pass # ok!

        paused = False

        if tab_queue.empty():
            log('Queue is empty. Exiting')
            return
        try:
            task = dict(tab_queue.get(block=True, timeout=10))
        except:
            log('ERROR! Queue raised error. Exiting')
            return
        task_no = task['task']
        # correct task
        task['full_load'] = task['full_load'] == 'True'
        if task.get('cleanup', '') == 'True':
            task['cleanup'] = True
        else:
            task['cleanup'] = False

        if task['start_id'] == "None":
            task['start_id'] = None
        if task['limit'] == "None":
            task['limit'] = None

        if task['cleanup']:
            cleanup = ' CLEANUP TABLE'
        else:
            cleanup = ''

        log('Processing task #{task}, table {table}, size {size}, full load {full_load}, '
            'start_id {start_id}. Queue size: {queue_size}'.format(queue_size=tab_queue.qsize(), **task) + cleanup)

        start_time = time.time()
        try:
            result = copy_records(src, dest,
                                  src_model_tables, dest_model_tables,
                                  tablename=task['table'],
                                  full_load=bool(task['full_load']),
                                  start_id=task['start_id'],
                                  limit=task['limit'],
                                  full_size=int(task['size']),
                                  task_no=task_no,
                                  journal_dir=journal_dir,
                                  packet_size=packet_size,
                                  cleanup=task['cleanup']
            )

        except Exception as e:
            log('ERROR CRITICAL! Copy process failed with message "%s"' % str(e))
            raise e
            continue  # TODO: stop load????

        if result is None:
            log('WARNING! Copy process returned empty result')
            continue

        total_time = time.time() - start_time
        task['total_time'] = '%.1f' % total_time
        if total_time != 0:
            task['rps'] = '%d' % (result / total_time)
        else:
            task['rps'] = '---'
        task['count'] = result
        log('Task #{task} done. Table {table}, {count} records in {total_time} seconds, rps {rps}'.format(**task))


def batch_move(processes_count, tasks_list, report_filename, journal_dir,
               src_params, dest_params,
               src_model, dest_model,
               packet_size=1000,
               do_create_schema=True,
               start_from=0,
               echo=False):

    if do_create_schema:
        dest = AConnector(dest_params['name'], dest_params['conn'], echo=echo, schema_name=dest_params['name'], encoding='utf8') # , encoding='utf8'
        print('Creating schema.')

        # TO DO: remove
        # dest.sql('DROP TABLE em_event')
        create_schema(dest, dest_params['name'], dest_model)

        del dest  # close connection
        #return

    if not os.path.exists(journal_dir):
        os.makedirs(journal_dir)

    print('Creating tables queue from %s' % tasks_list)
    with open(tasks_list, 'r') as f:
        q_list = json.loads(f.read())
    print('Total tasks count: %s' % len(q_list))

    if len(q_list) == 0:
        print('Tasklist is empty - exiting')

    if start_from != 0:
        print('Start from task %s' % start_from)
        q_list = [task for task in q_list if int(task['task']) >= start_from]
        print('Correct tasks count: %s' % len(q_list))

    if len(q_list) < processes_count:
        processes_count = len(q_list)

    with open(report_filename, 'a') as f:
        f.write('Starting: %s\n' % now())
        f.write('From %s:%s\n' % (src_params['name'], src_params['conn']))
        f.write('To %s:%s\n' % (dest_params['name'], dest_params['conn']))
        f.write('Base packet size: %s\n' % packet_size)
        f.write('Tasks list: %s\n' % tasks_list)
        f.write('Tasks count: %s\n' % len(q_list))
        f.write('Processes count: %s\n' % processes_count)
        # f.write('Threads count: %s\n' % threads_count)
        f.write('Journal dir: %s\n\n' % journal_dir)


    print('Copying data using %s processes' % processes_count)
    log_lock = multiprocessing.RLock()
    tab_queue = multiprocessing.Queue()
    for task in q_list:
        tab_queue.put_nowait(task)

    processes = []

    start_time = time.time()
    if processes_count > 1:
        for procnum in range(processes_count):
            proc = multiprocessing.Process(target=worker,
                                           name='worker_%02d' % (procnum+1),
                                           args=[tab_queue, log_lock,
                                                 src_params, dest_params,
                                                 src_model.SCHEMA_TABLES, dest_model.SCHEMA_TABLES,
                                                 report_filename, journal_dir,
                                                 packet_size
                                                 ])

            processes.append(proc)
            proc.start()


        for proc in processes:
            proc.join()
    else:
        worker(tab_queue, log_lock,
               src_params, dest_params,
               src_model.SCHEMA_TABLES, dest_model.SCHEMA_TABLES,
               report_filename, journal_dir,
               packet_size)

    print('Done in %d seconds' % (time.time() - start_time))
    exit(1)
