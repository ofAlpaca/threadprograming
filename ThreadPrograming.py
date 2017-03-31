import threading
import time
import queue
import logging

class SortList():
    def __init__(self, _list):
        self.List = _list
        self.index = 0
    def GetTopVal(self):
        if self.index == len(self.List):
            return None
        else :
            return self.List[self.index]
    def IndexPlus(self):
        self.index += 1
    def ResetIndex(self):
        self.index = 0

    @staticmethod
    def lenOfTotal(_list):
        sum = 0
        for i in _list:
            sum += len(i.List)
        return sum

def BubbleSort(_list, q):
   for i in range(len(_list)):
       for j in range(len(_list)-1-i):
           if _list[j] > _list[j+1]:
               _list[j], _list[j+1] = _list[j+1], _list[j] # swap
   q.put(_list)

def MergeSort(_ll, _rl, q): # both _ll and _rl are lists
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
        items.extend(_rl)
    else: # r == lenOf_rl
        items.extend(_ll)

    q.put(items)

def GetSepList(sepNum):
    file = open("input.txt","r")
    content = file.read()

    content_ls = content.split()
    # seprate the content by ' '
    lenOfcont = len(content_ls)

    int_con_ls = list(map(int, content_ls))
    # turn all content from string type to int type
    n = len(int_con_ls) // sepNum

    logging.warning('sepNum = ' + str(sepNum) + ', n = ' + str(n) + ' total = ' + str(lenOfcont))

    sep_ls = [int_con_ls[i:i+n] for i in range(0, n*sepNum, n)]
    # seprate the content_ls with n
    sep_ls[sepNum-1].extend(int_con_ls[n*sepNum:lenOfcont])
    # concate the rest of the content_ls to the last list
    return sep_ls

#----------------------------------------------------------

def main():
    threads = []
    m_threads = []
    sepNum = ''
    while not sepNum.isdigit():
         sepNum = input('Enter the number of threads: ')
    sepNum = int(sepNum)
    sep_list = GetSepList(sepNum)
    # get the processed sepratedly list
    q = queue.Queue(sepNum)
    # a queue to store several lists which are sorted by Bubblesort
    for i in range(sepNum):
        t = threading.Thread(name = 'bb_thread-' + str(i+1), target = BubbleSort, args = (sep_list[i], q))
        t.start()
        threads.append(t)

    cnt = 0
    while cnt != sepNum - 1:
        if q.qsize() >= 2:
            ll = q.get()
            rl = q.get()
            mt = threading.Thread(name = 'm_thread-' + str(i+1), target = MergeSort, args = (ll, rl, q))
            mt.start()
            m_threads.append(mt)
            cnt += 1
    
    print(q.get())
    print('Threading terminated...')
    time.sleep(3)

if __name__ == '__main__':
    main()
    
