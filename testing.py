import csv
from models import *
import matplotlib.pyplot as plt




# Jo's test, row 67, Lm=5150
'''
# test init
my_object = Tire(M=21, N=7.25, D=10, PR=10, SI=210, Lm=5150, IP=135, BL=15450, DoMax=21.25, DoMin=20.60,
                   WMax=7.20, WMin=6.80, DsMax=19.25, WsMax=6.35, AR=0.78, LR_RL=9, LR_BL=6.8, A=5.50, D2=10,
                   FH=1, G=1.4, DF=12, QS='TSO-C62')

Lm_databook = my_object.Lm
Lm_calc = my_object.max_load_capacity_calc()
print(f'From Databook: {Lm_databook}\nFrom Calculation: {Lm_calc}')
'''



# percentage error distribution
# Read data from the CSV file
file_path = 'manufacturer_data/tire_data.csv'
with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row

    percent_difference_list = []
    
    # Process each row
    for row in csv_reader:
        # Create an instance of MyClass using the row data
        my_object = Tire.from_row(row)

        try:
            Lm_databook = my_object.Lm
            Lm_calc = my_object.max_load_capacity_calc()
            percent_difference = abs(Lm_databook - Lm_calc) / Lm_databook * 100
        except TypeError:
            percent_difference = None
            
        percent_difference_list.append(percent_difference)

        # print(percent_difference_list)

# Filter out None values
filtered_percent_difference_list = [x for x in percent_difference_list if x is not None and x <= 200]

# Plotting the distribution graph
plt.hist(filtered_percent_difference_list, bins=10, edgecolor='black')

# Adding labels and title
plt.xlabel('Percent Difference')
plt.ylabel('Frequency')
plt.title('Distribution of Percent Differences')

# Displaying the plot
plt.show()





'''
#check correct reading of the csv file and class assignment

# Read data from the CSV file
file_path = 'manufacturer_data/tire_data.csv'
with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    
    # Access the desired row
    row_number = 65
    for index, row in enumerate(csv_reader):
        if index == row_number:
            my_object = Tire.from_row(row)
            attribute_list = [my_object.Pre,
            my_object.M, my_object.N, my_object.D, my_object.PR, my_object.SI, my_object.Lm, my_object.IP,
            my_object.BL, my_object.DoMax, my_object.DoMin, my_object.WMax, my_object.WMin, my_object.DsMax,
            my_object.WsMax, my_object.AR, my_object.LR_RL, my_object.LR_BL, my_object.A, my_object.D2,
            my_object.FH, my_object.G, my_object.DF, my_object.QS
            ]

print(attribute_list)


attribute_list_csv = ['',
    21, 7.25, 10, 10, 210, 5150, 135, 15450, 21.25, 20.6, 7.2, 6.8, 19.25, 6.35, 0.78,
    9, 6.8, 5.5, 10, 1, 1.4, 12, 'TSO-C62'
]
'''