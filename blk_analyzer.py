#from tkinter import Tk
#from tkinter.filedialog import askopenfilename
import sys
import numpy as np

def read_write_percentage(logs, complete):
    w_count = 0
    r_count = 0
    for i in logs:
        try:
            if 'W' in i[6]:
                w_count = w_count + 1
            elif 'R' in i[6]:
                r_count = r_count + 1
        except:
            print("No block reading or writing here. Skipping...")
    return r_count/len(logs) * 100, w_count/len(logs) * 100

def avg_block_size(logs):
    total = 0
    sector_size = 512   # bytes
    for i in logs:
        # read block size for each I/O request
        total = total + int(i[9])
    return (total / len(logs)) * sector_size

def unique_addresses(logs):
    unique = []
    unique_addr = open('unique_addr.txt', 'w')
    for i in logs:
        unique.append(i[7])
    # create a set to be able to recognize unique addresses
    unique_set = set(unique)
    #print(unique_set)
    number_of_unique_addresses = len(unique_set)
    #print("Number of Unique Addresses: {0}".format(number_of_unique_addresses))
    # a dictionary to hold address and its corresponding number of accesses
    addr_unique = {}
    for j in unique_set:
        addr_unique[j] = unique.count(j)
        unique_addr.write("Number of times address {0} was accessed: {1}\n".format(j, unique.count(j)))
        #print("Number of times address {0} was accessed: {1}".format(j, unique.count(j)))
    
    # sort out unique address dictionary
    addr_unique = dict(sorted(addr_unique.items(), key=lambda item: item[1]))
    unique_addr.write("\nNumber of all requests: {0}\nNumber of Unique Addresses: {1}\n"\
        .format(len(logs), number_of_unique_addresses))

    # mininum and maximum number of references
    min_access = addr_unique[min(addr_unique, key=addr_unique.get)]
    max_access = addr_unique[max(addr_unique, key=addr_unique.get)]
    # number of addresses with minimum/maximum references
    min_ref_addr = 0
    max_ref_addr = 0
    for address in addr_unique:
        if addr_unique[address] == min_access:
            min_ref_addr = min_ref_addr + 1
        elif addr_unique[address] == max_access:
            max_ref_addr = max_ref_addr + 1

    #print("Number of addresses with minimum access: {0}\nNumber of addresses with maximum access: {1}".format(min_ref_addr, max_ref_addr))
    unique_addr.write("Minimum number of access: {0}\nMaximum number of access: {1}\n"\
        .format(min_access, max_access))
    unique_addr.write("Number of addresses with minimum access: {0}\nNumber of addresses with maximum access: {1}\n"\
        .format(min_ref_addr, max_ref_addr))

    # mean & median of accesses
    addr_list = []
    for i in addr_unique:
        addr_list.append(addr_unique[i])
    print("Mean of accesses: {0}".format(np.mean(addr_list)))
    print("Median of accesses: {0}".format(np.median(addr_list)))
    unique_addr.write("\nmax_ref_addrMean of accesses: {0}\nMedian of accesses: {1}\n"\
        .format(np.mean(addr_list), np.median(addr_list)))

#Tk().withdraw()
#filename = askopenfilename()

#file_name = (filename)
file_name = sys.argv[1]

app_name = sys.argv[2]
#app_name = input('Enter the Application\'s name: ')
# a list of blktrace logs
total_io = []
# a list of all completed I/O requests
completed_io = []
complete = 0

# open the file
blK_file = open(file_name, 'r')

# a list of each separate I/O
io_row = blK_file.readline().split()
while True:
    # for those I/O with a specific process name (app_name)
    if app_name in io_row[-1]:
        if 'N' not in io_row[6]:
            total_io.append(io_row)
    # for completed I/O
    if '[0]' in io_row[-1]:
        completed_io.append(io_row)
        complete = complete + 1
    # start reading each line and appending it to total_io until the last line is reached. Then break.
    io_row = blK_file.readline().split()
    # this indicates the end of the log
    if "CPU" in io_row[0]:
        break

#for i in completed_io:
#    print(i)
#print("Total Number of Completed I/O Requests: {0}".format(complete))

# prints R/W percentage
#read_percent, write_percent = read_write_percentage(total_io, complete)
#print("Read Percentage: {0}%\nWrite Percentage: {1}%".format(read_percent, write_percent))

# prints average block size
#average_block_size = avg_block_size(total_io)
#print("Average Block Size: {0} Byte".format(average_block_size))

# prints the number of times a specific sector was accessed
unique_addresses(completed_io)