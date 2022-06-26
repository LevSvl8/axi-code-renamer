import json

if __name__ == '__main__':
    tasks_list = r'.\..\tasks\ora_hydro_42_task.json' # r'.\..\ora_hydro_42_task.json'

    try:
        with open(tasks_list, 'r') as f:
            q_list = json.loads(f.read())
    except:
        print("Can't open file %s" % tasks_list)
        exit(666)

    cnt = 0
    tabs = []
    for t in q_list:
        if t['table'] not in tabs:
            try:
                cnt += int(t['size'])
                tabs.append(t['table'])
            except:
                pass
    print('Total records count: %s' % cnt)