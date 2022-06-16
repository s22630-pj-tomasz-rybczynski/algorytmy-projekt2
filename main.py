from abc import abstractmethod
from distutils.command import build
import sys

logs = ''

class HuffNode(object):

    @abstractmethod
    def get_weight(self):
        pass

    @abstractmethod
    def is_leaf(self):
        pass

# leaf node is a node that doesn't have child nodes
class LeafNode(HuffNode):

    def __init__(self, value=0, freq=0):
        super().__init__()

        self.value = value
        self.weight = freq

    
    def is_leaf(self):
        return True

    def get_weight(self):
        return self.weight

    def get_value(self):
        return self.value

# internal node is a node that has child nodes
class IntlNode(HuffNode):

    def __init__(self, left_child=None, right_child=None):
        super().__init__()

        self.weight = left_child.get_weight() + right_child.get_weight()
        self.left_child = left_child
        self.right_child = right_child


    def is_leaf(self):
        return False

    def get_weight(self):
        return self.weight

    def get_left(self):
        return self.left_child

    def get_right(self):
        return self.right_child

class HuffTree(object):

    def __init__(self, flag, value=0, freq=0, left_tree=None, right_tree=None):
        super().__init__()

        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = IntlNode(left_tree.get_root(), right_tree.get_root())


    def get_root(self):
        return self.root

    def get_weight(self):
        return self.root.get_weight()

    def traverse_huffman_tree(self, root, code, char_freq): # change char_freq from char -> frequency, to char -> code
        if root.is_leaf():
            char_freq[root.get_value()] = code

            global logs
            logs += f'{chr(root.get_value())}={code} '
            
            return None
        else:
            self.traverse_huffman_tree(root.get_left(), code+'0', char_freq)
            self.traverse_huffman_tree(root.get_right(), code+'1', char_freq)


def min_heapify(A,k):
    l = 2 * k + 1
    r = 2 * k + 2

    if l < len(A) and A[l].get_weight() < A[k].get_weight():
        smallest = l
    else:
        smallest = k
    if r < len(A) and A[r].get_weight() < A[smallest].get_weight():
        smallest = r
    if smallest != k:
        A[k], A[smallest] = A[smallest], A[k]
        min_heapify(A, smallest)

def min_heap(A):
    for k in range(len(A)//2 - 1, -1, -1):
        min_heapify(A,k) 

# merge nodes using priority queue
def buildHuffmanTree(list_hufftrees):
    while len(list_hufftrees) > 1 :

        min_heap(list_hufftrees) # sort ascending by the weight

        new_hufftree = HuffTree(1, 0, 0, list_hufftrees.pop(0), list_hufftrees.pop(0))

        list_hufftrees.append(new_hufftree)

    return list_hufftrees.pop(0)


def compress(inputfilename, outputfilename):

    f = open(inputfilename,'rb') # read in binary format
    filedata = f.read()
    filesize = f.tell() # cursor position after reading the file

    char_freq = {} # unique list of chars saved as ascii dec -> frequency dec
    for x in range(filesize):
        tem = filedata[x]
        if tem in char_freq.keys():
            char_freq[tem] = char_freq[tem] + 1
        else:
            char_freq[tem] = 1


    list_hufftrees = []
    for x in char_freq.keys(): # foreach char append new HuffTree to a list
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)

    output = open(outputfilename, 'wb')

    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.get_root(), '', char_freq)

    global logs
    logs += '\n'
    output.write(bytes(logs, 'utf-8'))

    code = ''
    for i in range(filesize):
        key = filedata[i]
        code += char_freq[key]
        out = 0
        while len(code)>8: # convert 8 ones or zeros (1 byte) to dec number and then convert it to byte object
            for x in range(8):
                out = out<<1 
                if code[x] == '1':
                    out = out|1
            code = code[8:]
            output.write(bytes((out,)))
            out = 0


    out = 0
    for i in range(len(code)):
        out = out<<1
        if code[i]=='1':
            out = out|1

    output.write(bytes((out,)))
    output.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("please input the filenames")
        exit(0)
    else:
        INPUTFILE = sys.argv[1]
        OUTPUTFILE = sys.argv[2]

        compress(INPUTFILE, OUTPUTFILE)
 