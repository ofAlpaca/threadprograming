import threading
import time
import queue
import multiprocessing 
import logging
MSG_ASK_FOR_K = 'What is the value of k: '

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

logging.disable(logging.DEBUG)

def BubbleSort(_list, q):
    logging.debug('bbs-start')
    lenOfList = len(_list)
    for i in range(lenOfList):
        for j in range(lenOfList-1-i):
            if _list[j] > _list[j+1]:
                _list[j], _list[j+1] = _list[j+1], _list[j] # swap
    q.put(_list)
    logging.debug('bbs-end')

def MergeSort(_ll, _rl, q): # both _ll and _rl are lists
    logging.debug('ms-start')
    l, r = 0, 0
    lenOf_ll = len(_ll)
    lenOf_rl = len(_rl)
    items = []
    # selected index content can put here
    while l < lenOf_ll and r < lenOf_rl:
    # breaks if one of the list is empty !
        if _ll[l] < _rl[r]:
            items.append(_ll[l])
            l += 1
        else : # _ll[l] > _rl[r]
            items.append(_rl[r])
            r += 1

    if l == lenOf_ll:
        items.extend(_rl[r:lenOf_rl])
    else: # r == lenOf_rl
        items.extend(_ll[l:lenOf_ll])

    q.put(items)
    logging.debug('ms-end')

def Process_bubble_merge(_list, q):
    for l in _list:
        BubbleSort(l, q)

    while q.qsize() != 1:
        ll = q.get()
        rl = q.get()
        MergeSort(ll, rl, q)


def GetList(fileName, f):
    content = f.read()
    # read the rest of the data
    content_ls = content.split()
    # seprate the content by ' 
    int_con_ls = list(map(int, content_ls))
    # turn all content from string type to int type
    return int_con_ls

def GetSepList(fileName, sepNum, f):
    int_con_ls = GetList(fileName, f)
    lenOfcont = len(int_con_ls)
    n = len(int_con_ls) // sepNum

    sep_ls = [int_con_ls[i:i+n] for i in range(0, n*sepNum, n)]
    # seprate the content_ls with n
    sep_ls[sepNum-1].extend(int_con_ls[n*sepNum:lenOfcont])
    # concate the rest of the content_ls to the last list

    return sep_ls

def WriteFile(fileName, list, perf_time):
    fileName = fileName[0:len(fileName) - 4]
    file = open(fileName + '_output.txt', "w")
    
    file.write('Sorted:\n')
    for index in list:
        file.write(str(index) + ' ')
    file.write('\ntotal time : {:.5f} seconds'.format(perf_time))
    file.close()

#----------------------------------------------------------

def problem1(fileName,f):
    _list = GetList(fileName,f)
    q = queue.Queue(len(_list))

    start = time.perf_counter()
    # clock start
    BubbleSort(_list,q)
    # Start bubblesort function
    process_time = time.perf_counter() - start
    # clock end
    print('Time: ' + str(process_time))
    WriteFile(fileName, q.get(), process_time)

def problem2(fileName,f):
    threads = []
    m_threads = []
    sepNum = ''

    while not sepNum.isdigit():
         sepNum = input(MSG_ASK_FOR_K)
    sepNum = int(sepNum)
    sep_list = GetSepList(fileName, sepNum, f)
    # get the processed sepratedly list
    q = queue.Queue(sepNum)
    # a queue to store several lists which are sorted by Bubblesort

    i,j = 0,0
    for i in range(sepNum):
        t = threading.Thread(name = 'bb_t' + str(i), target=BubbleSort, args=(sep_list[i], q))
       # t.start()
        threads.append(t)

    start = time.perf_counter()
    # clock start
    cnt,t = 0,0
    while t < sepNum or cnt < sepNum - 1: # to the k - 1 thread
        # size of q is larger than 2
        if t < sepNum:
            threads[t].start()
            t += 1
        if q.qsize() >= 2:
            ll = q.get()
            rl = q.get()
            mt = threading.Thread(name = 'm_t' + str(cnt), target=MergeSort, args=(ll, rl, q))
            mt.start()
            m_threads.append(mt)
            cnt += 1

    for m in m_threads:
        m.join()
    

    process_time = time.perf_counter() - start
    # clock end
    print('Time: ' + str(process_time))
    WriteFile(fileName, q.get(), process_time)

def problem3(fileName, f):
    processes = []
    m_processes = []
    sepNum = ''

    while not sepNum.isdigit():
         sepNum = input(MSG_ASK_FOR_K)
    sepNum = int(sepNum)
    sep_list = GetSepList(fileName, sepNum, f)
    # get the processed sepratedly list
    manager = multiprocessing.Manager()
    q = manager.Queue(sepNum)
    # a queue to store several lists which are sorted by Bubblesort

    for i in range(sepNum):
        p = multiprocessing.Process(name ='bb_p' + str(i + 1), target=BubbleSort, args=(sep_list[i], q))
        #p.start()
        processes.append(p)

    start = time.perf_counter()
    # clock start
    cnt, p = 0,0
    while p < sepNum or cnt < sepNum - 1:
        if p < sepNum:
            processes[p].start()
            p += 1
        if q.qsize() >= 2:
            ll = q.get()
            rl = q.get()
            mp = multiprocessing.Process(name='m_p' + str(cnt + 1), target=MergeSort, args=(ll, rl, q))
            mp.start()
            m_processes.append(mp)
            cnt += 1

    for mp in m_processes:
        mp.join()

    process_time = time.perf_counter() - start
    print('Time: ' + str(process_time))
    # clock end
    WriteFile(fileName, q.get(), process_time)


def problem4(fileName, f):
    sepNum = ''
    while not sepNum.isdigit():
        sepNum = input(MSG_ASK_FOR_K)
    sepNum = int(sepNum)
    sep_list = GetSepList(fileName, sepNum, f)
    # get the processed sepratedly list
    manager = multiprocessing.Manager()
    q = manager.Queue(sepNum)
    # a queue to store several lists which are sorted by Bubblesort

    start = time.perf_counter()
    # clock start

    pbm = multiprocessing.Process(target = Process_bubble_merge, args = (sep_list, q))
    pbm.start()
    pbm.join()

    process_time = time.perf_counter() - start
    # clock end
    print('Time: ' + str(process_time))
    WriteFile(fileName, q.get(), process_time)

if __name__ == '__main__':
    fileName = input('Enter a file name: ')
    f = open(fileName , "r")
    c = f.read(1)
    
    if c == '1':
        problem1(fileName, f)
    elif c == '2':
        problem2(fileName, f)
    elif c == '3':
        problem3(fileName, f)
    elif c == '4':
        problem4(fileName, f)
    else :
        assert 'File corrupted!...'


    print('Threading Terminated....')
    input()