#from tkinter import Tk
#from tkinter.filedialog import askopenfilename
import sys
import numpy as np
import time
import math

def read_write_percentage(logs):
    print("Calculating R/W Percentage...")
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
    print("Calculating Average Block Size...")
    total = 0
    sector_size = 512   # bytes
    for i in logs:
        # read block size for each I/O request
        try:
            total = total + int(i[9])
        except:
            total = total + 1
    return (total / len(logs)) * sector_size

def unique_addresses(logs):
    print("Calculating Unique Addresses...")
    unique = []
    unique_addr = open('unique_addr.txt', 'w')

    nonunique_time = time.time()
    addr_unique = {}
    for i in logs:
        unique.append(i[7])
        if i[7] in addr_unique:
            addr_unique[i[7]] += 1
        else:
            addr_unique[i[7]] = 1
    # create a set to be able to recognize unique addresses
    unique_set = set(unique)
    #print("---Nonunique Time: %s seconds ---" % (time.time() - nonunique_time))

    #print(unique_set)
    number_of_unique_addresses = len(unique_set)
    #print("Number of Unique Addresses: {0}".format(number_of_unique_addresses))
    # a dictionary to hold address and its corresponding number of accesses
    unique_count_time = time.time()
    temp = ''
    for key, value in addr_unique.items(): 
    #for j in unique_set:
        #addr_unique[j] = unique.count(j)
        temp +=  key + ' ' + str(value) + '\n'
        #unique_addr.write("Number of times address {0} was accessed: {1}\n".format(j, unique.count(j)))
        #print("Number of times address {0} was accessed: {1}".format(j, unique.count(j)))
    unique_addr.write('Address' + ' Access\n')
    unique_addr.write(temp)
    #print(addr_unique)
    #print(len(addr_unique))
    #print("---Unique Count Time: %s seconds ---" % (time.time() - unique_count_time))
     
    # sort out unique address dictionary
    sort_time = time.time()
    addr_unique = dict(sorted(addr_unique.items(), key=lambda item: item[1]))
    #print("---Sort Time: %s seconds ---" % (time.time() - sort_time))
    
    unique_addr.write("\nNumber of All Completed Requests: {0}\nNumber of Unique Completed Addresses: {1}\n"\
        .format(len(logs), number_of_unique_addresses))

    # mininum and maximum number of references
    minmax_time = time.time()
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
    #print("---Min/Max Time: %s seconds ---" % (time.time() - minmax_time))

    #print("Number of addresses with minimum access: {0}\nNumber of addresses with maximum access: {1}".format(min_ref_addr, max_ref_addr))
    unique_addr.write("Minimum number of access: {0}\nMaximum number of access: {1}\n"\
        .format(min_access, max_access))
    unique_addr.write("Number of addresses with minimum access: {0}\nNumber of addresses with maximum access: {1}\n"\
        .format(min_ref_addr, max_ref_addr))

    # mean & median of accesses
    median_time = time.time()
    addr_list = []
    for i in addr_unique:
        addr_list.append(addr_unique[i])
    #print("Mean of accesses: {0}".format(np.mean(addr_list)))
    #print("Median of accesses: {0}".format(np.median(addr_list)))
    unique_addr.write("\nMean of accesses: {0}\nMedian of accesses: {1}\n"\
        .format(np.mean(addr_list), np.median(addr_list)))
    #print("---Mean/Median Time: %s seconds ---" % (time.time() - median_time))
    unique_addr.close()

    return addr_unique, max_access, min_access

def address_distribution(sorted_addr, max, min):
    threshold = math.ceil(math.log(max, 2))
    addresss_access_distribution = {}
    for i in range(1, threshold+2):
        if i == 1:
            addresss_access_distribution['1'] = 0
        elif i == 2:
            addresss_access_distribution['2'] = 0
        else:
            addresss_access_distribution[str(int(math.pow(2, i-2)+1))+'-'+str(int(math.pow(2, i-1)))] = 0
    #print(addresss_access_distribution)
    distribution_list = list(addresss_access_distribution)
    #print(distribution_list)
    for key, value in sorted_addr.items():
        # address position in the distribution dictionary
        address_position = math.ceil(math.log(value, 2))
        addresss_access_distribution[distribution_list[address_position]] += 1
    #print(addresss_access_distribution)
    return addresss_access_distribution
        
            

def block_size_distribution(logs):
    print("Caclaulting Block Size Access Distribution...")
    print("'Block Size':[# of accesses, # of reads, # of writes]")
    distribution_dict = {}

    # initialize a dictionary of lists for blcok sizes
    for i in logs:
        try:
            distribution_dict[i[9]] = [0, 0, 0]
        except:
            distribution_dict['0'] = [0, 0, 0]

    for i in logs:
        try:
            # number of accesses
            if i[9] in distribution_dict:
                distribution_dict[i[9]][0] += 1
            else:
                distribution_dict[i[9]][0] = 1
            # type of accesses
            if 'W' in i[6]:
                distribution_dict[i[9]][2] += 1
            elif 'R' in i[6]:
                distribution_dict[i[9]][1] += 1
        except:
            if '0' in distribution_dict:
                distribution_dict['0'][0] += 1
            else:
                distribution_dict['0'][0] = 1
            if 'W' in i[6]:
                distribution_dict['0'][2] += 1
            elif 'R' in i[6]:
                distribution_dict['0'][1] += 1
    # sort out in ascending order
    distribution_dict = dict(sorted(distribution_dict.items(), key=lambda item: item[1]))
    #print(distribution_dict)
    return distribution_dict

#Tk().withdraw()
#filename = askopenfilename()

#file_name = (filename)
file_name = sys.argv[1]

# get the name of the applicatoin
#app_name = sys.argv[2]

# a list of blktrace logs
total_io = []
# a list of all completed I/O requests
completed_io = []
complete = 0

# open the file
blK_file = open(file_name, 'r')

start_time = time.time()

# a list of each separate I/O
io_row = blK_file.readline().split()
while True:
    #print(io_row)
    #total_io.append(io_row)
    #print(sys.getsizeof(total_io))
    #if len(io_row) == 0:
    #    break
    # for those I/O with a specific process name (app_name)
    #try:
        #if app_name in io_row[-1]:
        #    if 'N' not in io_row[6]:
        #        total_io.append(io_row)
    #except:
     #   break    
    # for completed I/O
    try:
        if '[0]' in io_row[-1]:
            completed_io.append(io_row)
            complete = complete + 1
    except:
        break
    
    io_row = blK_file.readline().split()
    # start reading each line and appending it to total_io until the last line is reached. Then break.
    # this indicates the end of the log
    #if "CPU" in io_row[0]:
    #    break

#for i in completed_io:
#    print(i)
#print("Total Number of Completed I/O Requests: {0}".format(complete))
#print(sys.getsizeof(total_io))
# Read/Write percentage
read_percent, write_percent = read_write_percentage(completed_io)
print("Read Percentage: {0}%\nWrite Percentage: {1}%".format(read_percent, write_percent))

# average block size
average_block_size = avg_block_size(completed_io)
print("Average Block Size: {0} Byte".format(average_block_size))

# the number of times a specific sector was accessed
unqiue_time = time.time()
unique_addr, max_access, min_access = unique_addresses(completed_io)
print("---Unique Addresses Time: %s seconds ---" % (time.time() - unqiue_time))

# distribution of address accbinesses
#address_distribution_time = time.time()
addr_distrib = address_distribution(unique_addr, max_access, min_access)
#print("---Address Distribution Calculation Time: %s seconds ---" % (time.time() - address_distribution_time))

# access percentage to a specific number of blocks (e.g., how many 4 block accesses?)
#block_distribution_time = time.time()
blk_size_distrib = block_size_distribution(completed_io)
#print("---Block Size Distribution Calculation Time: %s seconds ---" % (time.time() - block_distribution_time))

result_file = open('unique_addr.txt', 'a')
result_file.write("\nRead Percentage: {0}\nWrite Percentage: {1}\n".format(read_percent, write_percent))
result_file.write("Average Block Size: {0} Bytes\n".format(average_block_size))
result_file.close()

# write the information about distribution
distribution_info = open("distribution_info.txt", 'w')
temp = '\nNumber of Blocks Access Read(%) Write(%)\n'
for key, value in blk_size_distrib.items():
    temp += str(int(key)+1) + ' ' + str(value[0]) + ' ' + str(round((value[1]/value[0])*100, 2)) + ' ' + str(round((value[2]/value[0])*100, 2)) + '\n'
distribution_info.write(temp)
temp2 = '\nRange Distriubtion(%)\n'
for key, value in addr_distrib.items():
    temp2 += key + ' ' + str(round((value / len(completed_io))*100, 5)) + '\n'
#distribution_info.write("\nUnique Address Distribution:\n{0}".format(addr_distrib))
distribution_info.write(temp2)
distribution_info.close()

print("---Total Execution Time: %s seconds ---" % (time.time() - start_time))