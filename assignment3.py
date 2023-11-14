import sys
import pandas as pd

filename = sys.argv[1]
scheduler = sys.argv[2]
energy_efficient = len(sys.argv) > 3 and sys.argv[3] == "EE"
energy_efficient = True

output = []

def read_input_file(filename):
    try:
        with open(filename, 'r') as data:
            data=pd.read_csv(filename, sep=' ', header=None, names=['Tasks', 'Deadline', 1188, 918, 648, 384, 'idle'])
            return data
    
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
        return None

data = read_input_file(filename)  
      
def schedule_edf(data):
    sorted_deadline = data.sort_values(by=data.columns[1])
    sorted_deadline = sorted_deadline.iloc[:-1]
    sorted_deadline['period'] = 0
    sorted_deadline['time remaining'] = 0
    original_values = sorted_deadline.iloc[:, 1].to_dict()
    current_time = 1
    total_energy = 0
    idle_time = 0
    output = ""
    # print(current_time)
    # print(sorted_deadline)

    while current_time < data.iat[0,1]:
        # change the output format before submitting

        if(sorted_deadline.iat[0,7] > current_time):
            sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
            partial_execution = sorted_deadline.iat[0,7] - current_time
            if sorted_period.iat[0,7] < current_time:
                if sorted_period.iat[0,8] > partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} 1188 {partial_execution} {str(partial_execution * (data.iat[0,2])/1000)+'J'}\n"
                    total_energy += (partial_execution * (data.iat[0,2])/1000)
                    current_time += partial_execution
                    sorted_period.iat[0,8] = sorted_period.iat[0,8] - partial_execution
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
                
                elif sorted_period.iat[0,8] > 0 and sorted_period.iat[0,8] <= partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} 1188 {sorted_period.iat[0,8]} {str(sorted_period.iat[0,8] * (data.iat[0,2])/1000)+'J'}\n"
                    total_energy += (sorted_period.iat[0,8] * (data.iat[0,2])/1000)
                    current_time += sorted_period.iat[0,8]
                    sorted_period.iat[0,8] = 0
                    sorted_period.iat[0,7] += original_values[sorted_period.index[0]]
                    sorted_period.iat[0,1] += original_values[sorted_period.index[0]]
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
                
                elif sorted_period.iat[0,2] > partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} 1188 {partial_execution} {str(partial_execution * (data.iat[0,2])/1000)+'J'}\n"
                    total_energy += (partial_execution * (data.iat[0,2])/1000)
                    current_time += partial_execution
                    sorted_period.iat[0,8] = sorted_period.iat[0,2] - partial_execution
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
                
                elif sorted_period.iat[0,2] <= partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} 1188 {sorted_period.iat[0,2]} {str(sorted_period.iat[0,2] * (data.iat[0,2])/1000)+'J'}\n"
                    total_energy += (sorted_period.iat[0,2] * (data.iat[0,2])/1000)
                    current_time += sorted_period.iat[0,2]
                    sorted_period.iat[0,7] += original_values[sorted_period.index[0]]
                    sorted_period.iat[0,1] += original_values[sorted_period.index[0]]
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
            else:
                output += f"{current_time} IDLE IDLE {sorted_period.iat[0,7]-current_time} {str((sorted_period.iat[0,7]-current_time) * (data.iat[0,6])/1000)+'J'}\n"
                idle_time += (sorted_period.iat[0,7] - current_time)
                total_energy += ((sorted_period.iat[0,7]-current_time) * (data.iat[0,6])/1000)
                current_time += sorted_period.iat[0,7] - current_time
                sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                # print(current_time , idle_time)
                # print(sorted_deadline)
        else:
            if(sorted_deadline.iat[0,8] > 0):
                output += f"{current_time}, {sorted_deadline.iat[0,0]} 1188 {sorted_deadline.iat[0,8]} {str((sorted_deadline.iat[0,8]) * (data.iat[0,6])/1000)+'J'}\n"
                total_energy += (sorted_deadline.iat[0,8] * (data.iat[0,2])/1000)
                current_time += sorted_deadline.iat[0,8]
                sorted_deadline.iat[0,8] = 0
                sorted_deadline.iat[0,7] += original_values[sorted_deadline.index[0]]
                sorted_deadline.iat[0,1] += original_values[sorted_deadline.index[0]]
                sorted_deadline = sorted_deadline.sort_values(by=sorted_deadline.columns[1])
                # print(current_time)
                # print(sorted_deadline)
            else:
                output += f"{current_time} {sorted_deadline.iat[0,0]} 1188 {sorted_deadline.iat[0,2]} {str(sorted_deadline.iat[0,2] * (data.iat[0,2]/1000))+'J'}\n"
                total_energy += (sorted_deadline.iat[0,2] * (data.iat[0,2])/1000)
                current_time += sorted_deadline.iat[0,2]
                sorted_deadline.iat[0,7] += original_values[sorted_deadline.index[0]]
                sorted_deadline.iat[0,1] += original_values[sorted_deadline.index[0]]
                sorted_deadline = sorted_deadline.sort_values(by=sorted_deadline.columns[1])
                # print(current_time)
                # print(sorted_deadline)

    idle_time = (idle_time / current_time) * 100
    return idle_time, total_energy, output

def schedule_rm(data):
    sorted_deadline = data.sort_values(by=data.columns[1])
    sorted_deadline = sorted_deadline.iloc[:-1]
    sorted_deadline['period'] = 0
    sorted_deadline['time remaining'] = 0
    original_values = sorted_deadline.iloc[:, 1].to_dict()
    sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
    current_time = 1
    total_energy = 0
    idle_time = 0
    remaining_time = 0
    output = ""
    # print("Current time:\n", current_time)
    # print("Sorted by deadline:\n", sorted_deadline)
    # print("Sorted by period:\n", sorted_period)

    while current_time < data.iat[0, 1]:

        active_tasks = sorted_deadline[sorted_deadline['period'] <= current_time]
        priority_list = sorted_period[sorted_period['period'] > current_time]
        #print("CURRENT TIME\n", current_time)
        #print("Sorted by deadline:\n", sorted_deadline)     
        #print("READY LIST\n", active_tasks)
        #print("PRIORITY LIST\n", priority_list)

        if active_tasks.empty:
            output += f"{current_time} IDLE IDLE {priority_list.iat[0,7] - current_time} {str((priority_list.iat[0,7]-current_time) * (data.iat[0,6])/1000)+'J'}\n"
            idle_time += (priority_list.iat[0,7] - current_time)
            total_energy += ((priority_list.iat[0,7]-current_time) * (data.iat[0,6])/1000)
            current_time += priority_list.iat[0,7] - current_time
            # print("Current time:", current_time, "Idle time:", idle_time)
            # print("READY LIST\n", active_tasks)
            # print("PRIORITY LIST\n", priority_list)


        else:
            priority_check = 0 if priority_list.empty else priority_list.iat[0,7]
            if(0 < priority_check - current_time < active_tasks.iat[0,2]):
                partial_execution =  priority_list.iat[0,7] - current_time
                if active_tasks.iat[0,8] > partial_execution:
                    remaining_time = partial_execution
                    active_tasks.iat[0,8] -= remaining_time 
                elif 0 < active_tasks.iat[0,8] <= partial_execution:
                    remaining_time = active_tasks.iat[0,8]
                    active_tasks.iat[0,8] = 0
                elif active_tasks.iat[0,2] > partial_execution:
                    remaining_time = partial_execution
                    active_tasks.iat[0,8] = active_tasks.iat[0,2] - remaining_time
                elif active_tasks.iat[0,2] <= partial_execution:
                    remaining_time = active_tasks.iat[0,2]
                output += f"{current_time} {active_tasks.iat[0,0]} 1188 {remaining_time} {str(remaining_time * (data.iat[0,2])/1000)+'J'}\n"
                total_energy += (remaining_time * (data.iat[0,2])/1000)
                current_time += remaining_time
                if active_tasks.iat[0,8] == 0:
                    sorted_deadline.loc[active_tasks.index[0],'period'] += original_values[active_tasks.index[0]]
                sorted_deadline.loc[active_tasks.index[0],'time remaining'] = active_tasks.iat[0,8]
                sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
                priority_list = sorted_period[sorted_period['period'] > current_time]
                #print("Current time:\n", current_time, "Task executed:", active_tasks.iat[0,0])
                active_tasks = sorted_deadline[sorted_deadline['period'] <= current_time]
                # print("READY LIST\n", active_tasks)
                # print("PRIORITY LIST\n", priority_list)
                # print("Sorted by deadline:\n", sorted_deadline)


            else:
                if(active_tasks.iat[0,8] > 0):
                    output += f"{current_time}, {active_tasks.iat[0,0]} 1188 {active_tasks.iat[0,8]} {str((active_tasks.iat[0,8]) * (data.iat[0,2])/1000)+'J'}\n"
                    total_energy += (active_tasks.iat[0,8] * (data.iat[0,2])/1000)
                    current_time += active_tasks.iat[0,8]
                    active_tasks.iat[0,8] = 0
                    sorted_deadline.loc[active_tasks.index[0],'time remaining'] = active_tasks.iat[0,8]
                    sorted_deadline.loc[active_tasks.index[0],'period'] += original_values[active_tasks.index[0]]
                    sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
                    priority_list = sorted_period[sorted_period['period'] > current_time]
                    #print("Current time:\n", current_time, "Task executed:", active_tasks.iat[0,0])
                    active_tasks = sorted_deadline[sorted_deadline['period'] <= current_time]
                    # print("READY LIST\n", active_tasks)
                    # print("PRIORITY LIST\n", priority_list)
                    # print("Sorted by deadline:\n", sorted_deadline)

                else:
                    output += f"{current_time} {active_tasks.iat[0,0]} 1188 {active_tasks.iat[0,2]} {str(active_tasks.iat[0,2] * (data.iat[0,2]/1000))+'J'}\n"
                    total_energy += (active_tasks.iat[0,2] * (data.iat[0,2])/1000)
                    current_time += active_tasks.iat[0,2]
                    sorted_deadline.loc[active_tasks.index[0],'period'] += original_values[active_tasks.index[0]]
                    sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
                    priority_list = sorted_period[sorted_period['period'] > current_time]
                    #print("Current time:\n", current_time, "Task executed:", active_tasks.iat[0,0])
                    active_tasks = sorted_deadline[sorted_deadline['period'] <= current_time]
                    # print("READY LIST\n", active_tasks)
                    # print("PRIORITY LIST\n", priority_list)
                    # print("Sorted by deadline:\n", sorted_deadline)


    idle_time = (idle_time / current_time) * 100
    return idle_time, total_energy, output

def max_efficiency():
    columns_to_multiply = data.columns[2:6]  
    first_element_values = data.iloc[0, 2:6] 
    data.iloc[1:, 2:6] = data.iloc[1:, 2:6].multiply(first_element_values, axis=1)
    data.iloc[1:, 2:6] = data.iloc[1:, 2:6] / 1000
    efficienct_freq = data.copy()
    print(efficienct_freq)
    data_subset = data.iloc[1:, :]

    # Calculate the percentage decrease for each pair of columns
    data_subset['decrease% 2 3'] = ((data_subset.iloc[:, 2] - data_subset.iloc[:, 3]) / data_subset.iloc[:, 2]) * 100
    data_subset['decrease% 2 4'] = ((data_subset.iloc[:, 2] - data_subset.iloc[:, 4]) / data_subset.iloc[:, 2]) * 100
    data_subset['decrease% 2 5'] = ((data_subset.iloc[:, 2] - data_subset.iloc[:, 5]) / data_subset.iloc[:, 2]) * 100

    # Now, data_subset contains three additional columns with the percentage decrease values, excluding the first row
    print(data_subset)

if energy_efficient:
    if scheduler == "EDF":
        max_efficiency()
    #elif scheduler == "RM":
        
elif scheduler == "EDF":
    idle_percentage, energy_consumption, schedule = schedule_edf(data)
    print(schedule)
    print("Schedule", scheduler, "energy consumption:", energy_consumption , "J\n")
    print("Schedule", scheduler, "idle percentage:", idle_percentage, "%\n")
elif scheduler == "RM":
    idle_percentage, energy_consumption, schedule = schedule_rm(data)
    print(schedule)
    print("Schedule", scheduler, "energy consumption:", energy_consumption , "J\n")
    print("Schedule", scheduler, "idle percentage:", idle_percentage, "%\n")
else:
    print("Invalid scheduling algorithm.")
    sys.exit(1)