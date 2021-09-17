from __future__ import division
import glob
#from tqdm import tqdm
import math
import os


if not os.path.exists('Results'):
    os.makedirs('Results')

csv_lists = []
#output_file = open("output.txt", "w")
#output_file.write("Workload\tTotal Number of Rows\tRead Percentage\tWrite Percentage\tAverage Request Size\tNumber of Distinct Addresses\n")
#output_file.close()

def calculate_request_type(reqs, last_iteration, last_iteration_length):
    global read, write, row_count, steps_reqs
    read = 0
    write = 0
    # for j in tqdm (range (100), desc="Calculating Read & Write Percentage...", position=0, leave=True): 
    for i in reqs:
        if i == 'Read':
            read = read + 1
        elif i == 'Write':
            write = write + 1
            
    if last_iteration == False:
        return round((read/steps_reqs)*100, 2), round((write/steps_reqs)*100, 2)
    else:
        return round((read/last_iteration_length)*100, 2), round((write/last_iteration_length)*100, 2)

def calculate_request_addr(reqs):
    global unique_list
    for i in reqs:
        if i not in unique_list:
            unique_list.append(i)
    return len(unique_list)

def calculate_request_size(reqs, last_iteration, last_iteration_length):
    global row_count, steps_reqs
    avg_size = 0
    for i in reqs:
        avg_size = avg_size + int(i)
    if last_iteration == False:
        return round(avg_size/steps_reqs, 2)
    else:
        return round(avg_size/last_iteration_length, 2)

interval = 10 #min

for file in glob.glob("*.csv"):
    csv_lists.append(file)

for csv in csv_lists:
    file = open(csv, "r")
    workload_specific_out = open("Results/"+csv.strip('.csv')+".txt", "w")
    workload_specific_out.write("Step\tNumber of Requests per Step\tRead Percentage\tWrite Percentage\tAverage Request Size\tNumber of Distinct Addresses\n")
    workload_specific_out.close()
    file_list = file.read().split('\n')
    req_type = []
    req_addr = []
    req_size = []
    read = 0
    write = 0
    row_count = 0
    unique_list = [] 
    for i in file_list[:-1]:
        row_count = row_count + 1
        req_type.append(i.split(',')[3])
        req_addr.append(i.split(',')[4])
        req_size.append(i.split(',')[5])
    steps_reqs = round((row_count/10080)*interval)
    file.close()
    iterations = int(math.floor(row_count/steps_reqs))
    workload_specific_out = open("Results/"+csv.strip('.csv')+".txt", "a")
    for i in range(0, iterations+1):
        workload_specific_out.write(str(i))
        workload_specific_out.write("\t")
        workload_specific_out.write(str(steps_reqs))
        if i == iterations:
            read_percetnage, write_percentage = calculate_request_type(req_type[i*steps_reqs:row_count], True, row_count-(iterations)*steps_reqs)
            distinct_addr = calculate_request_addr(req_addr[i*steps_reqs:row_count])
            avg_req_size = calculate_request_size(req_size[i*steps_reqs:row_count], True, row_count-(iterations)*steps_reqs)
        else:
            read_percetnage, write_percentage = calculate_request_type(req_type[i*steps_reqs:((i+1)*steps_reqs-1)], False, 0)
            distinct_addr = calculate_request_addr(req_addr[i*steps_reqs:((i+1)*steps_reqs-1)])
            avg_req_size = calculate_request_size(req_size[i*steps_reqs:((i+1)*steps_reqs-1)], False, 0)

        workload_specific_out.write("\t{}\t{}\t{}\t{}\n".format(read_percetnage, write_percentage, avg_req_size, distinct_addr))    

    workload_specific_out.close()
    # output_file = open("output.txt", "a")
    # output_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(csv.strip(".csv"), row_count, read_percetnage, write_percentage, avg_req_size, distinct_addr))
    # output_file.close()
