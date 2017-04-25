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

Wait

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
