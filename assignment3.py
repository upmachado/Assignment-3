import sys
import pandas as pd

filename = sys.argv[1]
scheduler = sys.argv[2]
energy_efficient = len(sys.argv) > 3 and sys.argv[3] == "EE"
output = []

def read_input_file(filename):
    try:
        with open(filename, 'r') as data:
            data=pd.read_csv(filename, sep=' ', header=None, names=['Tasks', 'Deadline', 625, 447, 307, 212, 'idle'])
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
    if not energy_efficient:
        sorted_deadline['power'] = int(data.iat[0,2])
        sorted_deadline['frequency'] = 1188
    original_values = sorted_deadline.iloc[:, 1].to_dict()
    current_time = 1
    total_energy = 0
    idle_time = 0
    output = ""
    missed_deadline = False
    # print(current_time)
    # print(sorted_deadline)

    while current_time < data.iat[0,1]:
        # change the output format before submitting
        active_tasks = sorted_deadline[sorted_deadline['period'] <= current_time]
        #print(active_tasks)
        if not active_tasks.empty:
            for index, row in active_tasks.iterrows():
                if row.iat[1] < current_time and row.iat[7]<current_time and row.iat[1]>row.iat[7]:
                    missed_deadline = True
                    return 0, 0, "Deadline missed", missed_deadline

        if sorted_deadline.iat[0,2] + current_time > data.iat[0,1] and sorted_deadline.iat[0,7] < current_time:
            partial_execution = data.iat[0,1] - current_time
            output += f"{current_time} {sorted_deadline.iat[0,0]} {sorted_deadline.iat[0,10]} {partial_execution} {str(partial_execution * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
            total_energy += (partial_execution * (sorted_deadline.iat[0,9])/1000)
            current_time += partial_execution
            # print(current_time)
            # print(sorted_deadline)

        elif(sorted_deadline.iat[0,7] > current_time):
            sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
            partial_execution = sorted_deadline.iat[0,7] - current_time
            if sorted_period.iat[0,7] < current_time:
                if sorted_period.iat[0,8] > partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} {sorted_deadline.iat[0,10]} {partial_execution} {str(partial_execution * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                    total_energy += (partial_execution * (sorted_deadline.iat[0,9])/1000)
                    current_time += partial_execution
                    sorted_period.iat[0,8] = sorted_period.iat[0,8] - partial_execution
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
                
                elif sorted_period.iat[0,8] > 0 and sorted_period.iat[0,8] <= partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} {sorted_deadline.iat[0,10]} {sorted_period.iat[0,8]} {str(sorted_period.iat[0,8] * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                    total_energy += (sorted_period.iat[0,8] * (sorted_deadline.iat[0,9])/1000)
                    current_time += sorted_period.iat[0,8]
                    sorted_period.iat[0,8] = 0
                    sorted_period.iat[0,7] += original_values[sorted_period.index[0]]
                    sorted_period.iat[0,1] += original_values[sorted_period.index[0]]
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
                
                elif sorted_period.iat[0,2] > partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} {sorted_deadline.iat[0,10]} {partial_execution} {str(partial_execution * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                    total_energy += (partial_execution * (sorted_deadline.iat[0,9])/1000)
                    current_time += partial_execution
                    sorted_period.iat[0,8] = sorted_period.iat[0,2] - partial_execution
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
                
                elif sorted_period.iat[0,2] <= partial_execution:
                    output += f"{current_time} {sorted_period.iat[0,0]} {sorted_deadline.iat[0,10]} {sorted_period.iat[0,2]} {str(sorted_period.iat[0,2] * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                    total_energy += (sorted_period.iat[0,2] * (sorted_deadline.iat[0,9])/1000)
                    current_time += sorted_period.iat[0,2]
                    sorted_period.iat[0,7] += original_values[sorted_period.index[0]]
                    sorted_period.iat[0,1] += original_values[sorted_period.index[0]]
                    sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                    # print(current_time)
                    # print(sorted_deadline)
            else:
                output += f"{current_time} IDLE IDLE {sorted_period.iat[0,7]-current_time} {str((sorted_period.iat[0,7]-current_time) * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                idle_time += (sorted_period.iat[0,7] - current_time)
                total_energy += ((sorted_period.iat[0,7]-current_time) * (data.iat[0,6])/1000)
                current_time += sorted_period.iat[0,7] - current_time
                sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                # print(current_time , idle_time)
                # print(sorted_deadline)
        else:
            if(sorted_deadline.iat[0,8] > 0):
                output += f"{current_time}, {sorted_deadline.iat[0,0]} {sorted_deadline.iat[0,10]} {sorted_deadline.iat[0,8]} {str((sorted_deadline.iat[0,8]) * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                total_energy += (sorted_deadline.iat[0,8] * (sorted_deadline.iat[0,9])/1000)
                current_time += sorted_deadline.iat[0,8]
                sorted_deadline.iat[0,8] = 0
                sorted_deadline.iat[0,7] += original_values[sorted_deadline.index[0]]
                sorted_deadline.iat[0,1] += original_values[sorted_deadline.index[0]]
                sorted_deadline = sorted_deadline.sort_values(by=sorted_deadline.columns[1])
                # print(current_time)
                # print(sorted_deadline)
            else:
                output += f"{current_time} {sorted_deadline.iat[0,0]} {sorted_deadline.iat[0,10]} {sorted_deadline.iat[0,2]} {str(sorted_deadline.iat[0,2] * ((sorted_deadline.iat[0,9]))/1000)+'J'}\n"
                total_energy += (sorted_deadline.iat[0,2] * (sorted_deadline.iat[0,9])/1000)
                current_time += sorted_deadline.iat[0,2]
                sorted_deadline.iat[0,7] += original_values[sorted_deadline.index[0]]
                sorted_deadline.iat[0,1] += original_values[sorted_deadline.index[0]]
                sorted_deadline = sorted_deadline.sort_values(by=sorted_deadline.columns[1])
                # print(current_time)
                # print(sorted_deadline)

    idle_time = (idle_time / current_time) * 100
    return idle_time, total_energy, output, missed_deadline

def schedule_rm(data):
    sorted_deadline = data.sort_values(by=data.columns[1])
    sorted_deadline = sorted_deadline.iloc[:-1]
    sorted_deadline['period'] = 0
    sorted_deadline['time remaining'] = 0
    if not energy_efficient:
        sorted_deadline['power'] = data.iat[0,2]
        sorted_deadline['frequency'] = 1188
    original_values = sorted_deadline.iloc[:, 1].to_dict()
    sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
    current_time = 1
    total_energy = 0
    idle_time = 0
    remaining_time = 0
    output = ""
    missed_deadline = False
    # print("Current time:\n", current_time)
    # print("Sorted by deadline:\n", sorted_deadline)
    # print("Sorted by period:\n", sorted_period)

    while current_time < data.iat[0, 1]:


        active_tasks = sorted_deadline[sorted_deadline['period'] <= current_time]
        priority_list = sorted_period[sorted_period['period'] > current_time]
        #print("CURRENT TIME:", current_time)
        # print("Sorted by deadline:\n", sorted_deadline)     
        # print("READY LIST\n", active_tasks)
        # print("PRIORITY LIST\n", priority_list)
        if not active_tasks.empty:
            for index, row in active_tasks.iterrows():
                if row.iat[1] < current_time and row.iat[7]<current_time and row.iat[1]>row.iat[7]:
                    missed_deadline = True
                    return 0, 0, "Deadline missed", missed_deadline

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
            if active_tasks.iat[0,2] + current_time > data.iat[0,1]:
                partial_execution = data.iat[0,1] - current_time
                output += f"{current_time} {active_tasks.iat[0,0]} {sorted_deadline.iat[0,10]} {partial_execution} {str(partial_execution * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                total_energy += (partial_execution * (sorted_deadline.iat[0,9])/1000)
                current_time += partial_execution
                print("Current time:\n", current_time, "Task executed:", active_tasks.iat[0,0])
                print("READY LIST\n", active_tasks)
                print("PRIORITY LIST\n", priority_list)
                print("Sorted by deadline:\n", sorted_deadline)
            
            elif(0 < priority_check - current_time < active_tasks.iat[0,2]):
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
                output += f"{current_time} {active_tasks.iat[0,0]} {sorted_deadline.iat[0,10]} {remaining_time} {str(remaining_time * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                total_energy += (remaining_time * (sorted_deadline.iat[0,9])/1000)
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
                    output += f"{current_time}, {active_tasks.iat[0,0]} {sorted_deadline.iat[0,10]} {active_tasks.iat[0,8]} {str((active_tasks.iat[0,8]) * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                    total_energy += (active_tasks.iat[0,8] * (sorted_deadline.iat[0,9])/1000)
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
                    output += f"{current_time} {active_tasks.iat[0,0]} {sorted_deadline.iat[0,10]} {active_tasks.iat[0,2]} {str(active_tasks.iat[0,2] * (sorted_deadline.iat[0,9])/1000)+'J'}\n"
                    total_energy += (active_tasks.iat[0,2] * (sorted_deadline.iat[0,9])/1000)
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
    return idle_time, total_energy, output, missed_deadline

def max_efficiency(data):
    data['period'] = 0
    data['time remaining'] = 0
    data['power'] = int(data.iat[0,2])
    data['frequency'] = 1188
    frequency_list = [1188, 918, 648, 384]
    idle_percentage, energy_consumption, schedule, missed_deadline = schedule_edf(data)
    idle_time = idle_percentage * data.iat[0, 1] / 100
    #print("Idle time:", idle_time, "Energy consumption:", energy_consumption, "J\n")
    print("Data:\n", data)
    original_data = data.copy()

    data_energy_consumed = data.iloc[1:, :].copy()
    data_energy_consumed.loc[1:,625:212] = (data_energy_consumed.loc[1:,625:212] * data.loc[0, 625:212]).astype(int)
    data_energy_consumed.loc[1:,625:212] = (data_energy_consumed.loc[1:,625:212] / 1000).astype(float)  # Explicitly cast to float'
    #print("Energy by task:\n", data_energy_consumed)
    subtracted_values = data.iloc[1:, :].copy()
    subtracted_values.drop(subtracted_values.columns[3:11], axis=1, inplace=True)
    subtracted_values[447] = (((data_energy_consumed.loc[1:,625] - data_energy_consumed.loc[1:,447]) / data_energy_consumed.loc[1:, 625]) * 100).astype(float)
    subtracted_values[307] = (((data_energy_consumed.loc[1:,625] - data_energy_consumed.loc[1:,307]) / data_energy_consumed.loc[1:, 625]) * 100).astype(float)
    subtracted_values[212] = (((data_energy_consumed.loc[1:,625] - data_energy_consumed.loc[1:,212]) / data_energy_consumed.loc[1:, 625]) * 100).astype(float)
    #print("Percent change by task:\n", subtracted_values)
    
    data_wcet_change = data.iloc[1:, :].copy()
    data_wcet_change.drop(data_wcet_change.columns[3:11], axis=1, inplace=True)
    data_wcet_change[447] = (data.loc[1:,447] - data.loc[1:,625]).astype(float)
    data_wcet_change[307] = (data.loc[1:,307] - data.loc[1:,625]).astype(float)
    data_wcet_change[212] = (data.loc[1:,212] - data.loc[1:,625]).astype(float)

    data_wcet_change['Executions'] = (data.iat[0, 1] / data_wcet_change.loc[:, 'Deadline']).round()
    data_wcet_change[447] = data_wcet_change.loc[1:,447]  * data_wcet_change['Executions']
    data_wcet_change[307] = data_wcet_change.loc[1:,307]  * data_wcet_change['Executions']
    data_wcet_change[212] = data_wcet_change.loc[1:,212]  * data_wcet_change['Executions']
    #print("Execution Time Change:\n", data_wcet_change)

    subtracted_values['max_value'] = subtracted_values.iloc[:, 4:6].max(axis=1)
    subtracted_values = subtracted_values.sort_values(by='max_value', ascending=False)
    print("Max values:\n", subtracted_values)
    max_index = subtracted_values.iloc[:, 3:6].idxmax(axis=1)
    #print("Max values:\n", max_index)
    max_values = data.loc[max_index.index, max_index.values]
    print("Most efficient values:\n", max_values)
    print("Data:\n", data)
    max_column_name = max_values.idxmax(axis=1).values[0]
    print("Most efficient task:", max_column_name)
    data.loc[max_index.index[0],625] = max_values.iat[0,0]
    data.loc[max_index.index[0],'power'] = max_column_name
    print("Data:\n", data)
    idle_percentage, energy_consumption, schedule, missed_deadline = schedule_edf(data)


    return idle_percentage, energy_consumption, schedule, missed_deadline


if energy_efficient:
    if scheduler == "EDF":
        idle_percentage, energy_consumption, schedule, missed_deadline = max_efficiency(data)
        print(schedule)
        print("Schedule", scheduler,". Energy consumption:", energy_consumption , "J\n")
        print("System Execution time:", data.iat[0,1],". Idle percentage:", idle_percentage, "%\n")
    elif scheduler == "RM":
        idle_percentage, energy_consumption, schedule, missed_deadline = max_efficiency(data)
        print(schedule)
        print("Schedule", scheduler,". Energy consumption:", energy_consumption , "J\n")
        print("System Execution time:", data.iat[0,1],". Idle percentage:", idle_percentage, "%\n")
        
elif scheduler == "EDF":
    idle_percentage, energy_consumption, schedule, missed_deadline = schedule_edf(data)
    print(schedule)
    print("Schedule", scheduler,". Energy consumption:", energy_consumption , "J\n")
    print("System Execution time:", data.iat[0,1],". Idle percentage:", idle_percentage, "%\n")
elif scheduler == "RM":
    idle_percentage, energy_consumption, schedule, missed_deadline = schedule_rm(data)
    print(schedule)
    print("Schedule", scheduler,". Energy consumption:", energy_consumption , "J\n")
    print("System Execution time:", data.iat[0,1],". Idle percentage:", idle_percentage, "%\n")
else:
    print("Invalid scheduling algorithm.")
    sys.exit(1)