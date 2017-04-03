import threading
import time
import queue
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                     )

logging.disable(logging.CRITICAL)

def BubbleSort(_list, q):
   logging.debug('starting')
   for i in range(len(_list)):
       for j in range(len(_list)-1-i):
           if _list[j] > _list[j+1]:
               _list[j], _list[j+1] = _list[j+1], _list[j] # swap
   q.put(_list)
   logging.debug(_list)
   logging.debug('exiting')

def MergeSort(_ll, _rl, q): # both _ll and _rl are lists
    logging.debug('starting')
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
    logging.debug(items)
    logging.debug('exiting')

def GetList(fileName):
    file = open(fileName + '.txt', "r")
    content = file.read()

    content_ls = content.split()
    # seprate the content by ' 
    int_con_ls = list(map(int, content_ls))
    # turn all content from string type to int type
    file.close()
    return int_con_ls

def GetSepList(fileName, sepNum):
    int_con_ls = GetList(fileName)
    lenOfcont = len(int_con_ls)
    n = len(int_con_ls) // sepNum

    logging.debug('sepNum:' + str(sepNum) + ', n:' + str(n) + ', total:' + str(lenOfcont))

    sep_ls = [int_con_ls[i:i+n] for i in range(0, n*sepNum, n)]
    # seprate the content_ls with n
    sep_ls[sepNum-1].extend(int_con_ls[n*sepNum:lenOfcont])
    # concate the rest of the content_ls to the last list
    for i in sep_ls:
        logging.debug(i)
    return sep_ls

def WriteFile(fileName, list, perf_time):
    file = open(fileName + '_output.txt', "w")
    
    for index in list:
        file.write(str(index) + ' ')
    file.write('total time : {:.5f} seconds'.format(perf_time))
    file.close()

#----------------------------------------------------------

def main():
    threads = []
    m_threads = []
    sepNum = ''

    fileName = input('Which file would you want to sort: ')
    # while not os.path.isfile(fileName+'.txt'):
    while not sepNum.isdigit():
         sepNum = input('Enter the number of threads: ')
    sepNum = int(sepNum)
    
    sep_list = GetSepList(fileName, sepNum)
    # get the processed sepratedly list
    q = queue.Queue(sepNum)
    # a queue to store several lists which are sorted by Bubblesort

    start = time.perf_counter()
    time.clock()
    # set start to the begining timer
    for i in range(sepNum):
        t = threading.Thread(name = 'bb_thread-' + str(i+1), target = BubbleSort, args = (sep_list[i], q))
        t.start()
        threads.append(t)

    cnt = 0
    while cnt != sepNum - 1:
        if q.qsize() >= 2:
            ll = q.get()
            rl = q.get()
            mt = threading.Thread(name = 'm_thread-' + str(cnt + 1), target = MergeSort, args = (ll, rl, q))
            mt.start()
            m_threads.append(mt)
            cnt += 1

    process_time = time.perf_counter() - start
    WriteFile(fileName, q.get(), process_time)
    # print('-> {:.5f}'.format(process_time) + ' seconds')
    print('Threading terminated...')
    time.sleep(3)

if __name__ == '__main__':
    main()
    
