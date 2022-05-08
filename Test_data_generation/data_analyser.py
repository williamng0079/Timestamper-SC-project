import os
import matplotlib.pyplot as plt
import sys

def calculate_avg(list):
    avg = sum(list)/len(list)
    return avg



def read_delay_data(continuous=False):
    if continuous == True:
        continuous_req_list =[]
        with open("../Timestamper-SC-project/Test_data_generation/Continuous_Delay.txt", "r") as testfile:
            data = testfile.readlines()
            for i in data:
                continuous_req_list.append(float(i))
        print(continuous_req_list)
        list_len = len(continuous_req_list)
        
        return continuous_req_list, list_len
    else:
        single_req_list = []
        with open("../Timestamper-SC-project/Test_data_generation/Single_Delay.txt", "r") as testfile:
            data = testfile.readlines()
            for i in data:
                single_req_list.append(float(i))
        print(single_req_list)
        list_len = len(single_req_list)
        return single_req_list, list_len


def read_gas_data():
    gas_usage_list = []
    with open("../Timestamper-SC-project/Test_data_generation/Gas_Usage.txt", "r") as testfile:
        data = testfile.readlines()
        for i in data:
            gas_usage_list.append(int(i))
        print(gas_usage_list)
        list_len = len(gas_usage_list)

        return gas_usage_list, list_len

def read_batch_delay_data():
    batch_delay_list = []
    with open("../Timestamper-SC-project/Test_data_generation/Batch_Delay.txt", "r") as testfile:
        data = testfile.readlines()
        for i in data:
            batch_delay_list.append(float(i))
        print(batch_delay_list)
        list_len = len(batch_delay_list)

        return batch_delay_list, list_len


def plot_time_delay(con=False):
    
    if con == True:
        x = 0
        dataset, data_length = read_delay_data(True)
        x_value = []
        for i in range(data_length):
            x = x+1
            x_value.append(x)
        #print(x_value)
        avg = calculate_avg(dataset)
        plt.plot(x_value,dataset, label="Average time delay = {}".format(avg))
        plt.ylabel("Time Delay of Continuous in Seconds")
        plt.xlabel("Number of Requests")
        plt.title("Continuous Requests (w/0.3s interval between requests)")
        plt.legend()
        plt.show()
    else:
        x = 0
        dataset, data_length = read_delay_data()
        x_value = []
        for i in range(data_length):
            x = x+1
            x_value.append(x)
        avg = calculate_avg(dataset)
        plt.plot(x_value, dataset, label="Average time delay = {}".format(avg))
        plt.ylabel("Time Delay of Transaction Requests in Seconds")
        plt.xlabel("Number of Requests")
        plt.title("Single Request per Block Generation")
        plt.legend()
        plt.show()


def plot_batch_delay():
        x = 0
        dataset, data_length = read_batch_delay_data()
        x_value = []
        for i in range(data_length):
            x = x+1
            x_value.append(x)
        plt.plot(x_value, dataset)
        plt.ylabel("Addtional Time Required to Process the Batch Timestamp List")
        plt.xlabel("Number of Hash within the batch timestamp list")
        plt.title("Process Time of n Number of Elements in the Batch Timestamp list ")
        plt.show()

def plot_gasUsage():
        x = 0
        dataset, data_length = read_gas_data()
        x_value = []
        for i in range(data_length):
            x = x+1
            x_value.append(x)
        gas_diff = dataset[1] - dataset[0] 
        plt.plot(x_value, dataset, label= "Increase in gas unit per additional element in list = {}".format(gas_diff))
        plt.ylabel("Gas Usage in Gas Units")
        plt.xlabel("Number of Hash within the batch timestamp list")
        plt.title("Gas Usage of Batch Timestamp ")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    os.system("clear")
    print("Which dataset would you like to visualise?")
    print("\n1. PLOT TIME DELAY DATA FOR SINGLE REQUEST PER BLOCK GENERATION")
    print("\n2. PLOT TIME DELAY DATA FOR CONTINUOUS REQUESTS")
    print("\n3. PLOT TIME DELAY DATA FOR BATCH TIMESTAMP LIST PER ADDITIONAL ELEMENT")
    print("\n4. PLOT GAS USAGE INCREASE PER ADDITIONAL ELEMENT IN BATCH TIMESTAMP LIST")

    userInput = input("\nInput>>>")
    if userInput == "1":
        plot_time_delay()
    elif userInput == "2":
        plot_time_delay(True)
    
    elif userInput == "3":
        plot_batch_delay()

    elif userInput == "4":
        plot_gasUsage()
    
    else:
        print("Unregistered Input please restart, terminating tests.......")
        sys.exit()
    
    
