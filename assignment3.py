import sys
import pandas as pd

filename = sys.argv[1]
scheduler = sys.argv[2]
energy_efficient = len(sys.argv) > 3 and sys.argv[3] == "EE"
output = []

def read_input_file(filename):
    try:
        with open(filename, 'r') as data:
            data=pd.read_csv(filename, sep=' ', header=None, names=['Tasks', 'Deadline', 1188, 918, 648, 384, 'idle'])
            return data
    
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
        return None

data = read_input_file(filename)  # Call the function with the variable 'filename'.
      
def schedule_edf():
    sorted_deadline = data.sort_values(by=data.columns[1])
    sorted_deadline = sorted_deadline.iloc[:-1]
    sorted_deadline['period'] = 0
    sorted_deadline['time remaining'] = 0
    original_values = sorted_deadline.iloc[:, 1].to_dict()
    current_time = 1
    output = ""
    print(sorted_deadline)

    while current_time < data.iat[0,1]:
        # change the output format before submitting

        while(sorted_deadline.iat[0, 7] > current_time):
            sorted_period = sorted_deadline.sort_values(by=sorted_deadline.columns[7])
            if sorted_period.iat[0,8] > 0:
                partial_execution = sorted_deadline.iat[0,7] - current_time
            else:
                partial_execution = sorted_deadline.iat[0,7] - current_time
            
            if sorted_period.iat[0,2] >= partial_execution and sorted_period.iat[0,8] == 0 and sorted_period.iat[0,7] < current_time:
                partial_execution = sorted_deadline.iat[0,7]-current_time
                output += f"{current_time}, {sorted_period.iat[0,0]}, 1188, {partial_execution}\n"
                current_time = sorted_deadline.iat[0,7]
                sorted_period.iat[0,8] = sorted_period.iat[0,2] - partial_execution
                sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                print(current_time)
                print(sorted_deadline)

            elif sorted_period.iat[0,2] < partial_execution and sorted_period.iat[0,8] == 0 and sorted_period.iat[0,7] < current_time:
                output += f"{current_time}, {sorted_period.iat[0,0]}, 1188, {partial_execution}\n" 
                current_time += partial_execution
                sorted_period.iat[0,8] = sorted_period.iat[0,8] - partial_execution
                if sorted_period.iat[0,8] == 0:
                    sorted_period.iat[0,7] += original_values[sorted_period.index[0]]
                    sorted_period.iat[0,1] += original_values[sorted_period.index[0]]
                sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                current_time = sorted_deadline.iat[0,7]
                print(current_time)
                print(sorted_deadline)

            elif sorted_period.iat[0,8] > 0 and sorted_period.iat[0,7] < current_time:
                output += f"{current_time}, {sorted_period.iat[0,0]}, 1188, {partial_execution}\n" 
                current_time += partial_execution
                sorted_period.iat[0,8] = sorted_period.iat[0,8] - partial_execution
                if sorted_period.iat[0,8] == 0:
                    sorted_period.iat[0,7] += original_values[sorted_period.index[0]]
                    sorted_period.iat[0,1] += original_values[sorted_period.index[0]]
                sorted_deadline = sorted_period.sort_values(by=sorted_period.columns[1])
                print(current_time)
                print(sorted_deadline)

            else:
                output += f'{current_time}, "Idle", "Idle", {sorted_deadline.iat[0,7]-current_time}\n'
                current_time = sorted_deadline.iat[0,7]
                print(current_time)
                print(sorted_deadline)

        if(sorted_deadline.iat[0,8] > 0):
            output += f"{current_time}, {sorted_deadline.iat[0,0]}, 1188, {sorted_deadline.iat[0,8]}\n"
            current_time = current_time + sorted_deadline.iat[0,8]
            sorted_deadline.iat[0,8] = 0
            sorted_deadline.iat[0,7] += original_values[sorted_deadline.index[0]]
            sorted_deadline.iat[0,1] += original_values[sorted_deadline.index[0]]
            sorted_deadline = sorted_deadline.sort_values(by=sorted_deadline.columns[1])
            print(current_time)
            print(sorted_deadline)

        else:
            #output.extend([current_time, sorted_deadline.iat[0,0], 1188, sorted_deadline.iat[0,2]])
            output += f"{current_time}, {sorted_deadline.iat[0,0]}, 1188, {sorted_deadline.iat[0,2]}\n"
            current_time = current_time + sorted_deadline.iat[0,2]
            sorted_deadline.iat[0,7] += original_values[sorted_deadline.index[0]]
            sorted_deadline.iat[0,1] += original_values[sorted_deadline.index[0]]
            sorted_deadline = sorted_deadline.sort_values(by=sorted_deadline.columns[1])
            print(current_time)
            print(sorted_deadline)

    return output

#def schedule_rm():

    
    #while current_time<data.iat[0,1]:

# Implement the scheduling algorithm based on user input
if scheduler == "EDF":
    schedule = schedule_edf()
elif scheduler == "RM":
    schedule = schedule_rm()
elif scheduler == "EE" and energy_efficient:
    schedule = schedule_ee_edf() if scheduler == "EDF" else schedule_ee_rm()
else:
    print("Invalid scheduling algorithm.")
    sys.exit(1)

print(schedule)
# Calculate energy consumption, idle time, and total execution time
#total_energy, idle_percentage, total_execution_time = calculate_metrics(schedule, power_settings, max_time)

# Write the scheduling results to the output file
#write_output_file("output.txt", schedule, total_energy, idle_percentage, total_execution_time)