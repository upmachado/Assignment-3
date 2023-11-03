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
    sorted_df = data.sort_values(by=data.columns[1])
    sorted_df = sorted_df.iloc[:-1]
    sorted_df['period'] = 0
    sorted_df['time remaining'] = 0
    original_values = sorted_df.iloc[:, 1].to_dict()
    current_time = 1
    output = ""
    print(sorted_df)

    while current_time<data.iat[0,1]:
        # change the output format before submitting
        if sorted_df.iat[0, 7] > current_time:
            for i in range(len(sorted_df)):
                if sorted_df.iat[i, 7] < current_time:
                    while(current_time>sorted_df.iat[0,7]):
                        sorted_df.iat[i,8] = sorted_df.iat[0,7]-current_time
                        current_time=sorted_df.iat[0,7]
                    output += f"{current_time}, {'idle'}, 1188, {sorted_df.iat[0,8]}\n"

            output += f"{current_time}, {'idle'}, 1188, {sorted_df.iat[0,1]-current_time}\n"
            current_time = sorted_df.iat[0,1]
            print(sorted_df)
            print(current_time)
        else:
            #output.extend([current_time, sorted_df.iat[0,0], 1188, sorted_df.iat[0,2]])
            output += f"{current_time}, {sorted_df.iat[0,0]}, 1188, {sorted_df.iat[0,2]}\n"
            current_time = current_time + sorted_df.iat[0,2]
            sorted_df.iat[0,7] += original_values[sorted_df.index[0]]
            sorted_df.iat[0,1] += original_values[sorted_df.index[0]]  # Update the deadline
            sorted_df = sorted_df.sort_values(by=data.columns[1])
            print(sorted_df)
                
        #print(sorted_df)
    print(output)

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

print(output)
# Calculate energy consumption, idle time, and total execution time
#total_energy, idle_percentage, total_execution_time = calculate_metrics(schedule, power_settings, max_time)

# Write the scheduling results to the output file
#write_output_file("output.txt", schedule, total_energy, idle_percentage, total_execution_time)