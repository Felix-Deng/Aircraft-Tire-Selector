import csv 
from models import Tire


# Retrieve given tire data 
with open("manufacturer_data/tire_data.csv") as data_csv: 
    csv_reader = csv.reader(data_csv)
    next(csv_reader)  # skip header row 
    for row in csv_reader: 
        """Column index: [
            'Pre', 'M', 'N', 'D', 'PR', 'SI', 'Lm', 'IP', 'BL', 
            'DoMax', 'DoMin', 'WMax', 'WMin', 'DsMax', 'WsMax', 
            'AR', 'LR_RL', 'LR_BL', 'A', 'D', 'FH', 'G', 'DF', 'QS'
        ]
        """
        # With every row of data, create a new Tire object to 
        # calculate maximum load capacity (Lm) 
        ##### Write your code below #####
        print(row)
        tire = Tire()
        break 
    
# Save the calculated Lm to a new CSV to compare with given 
# manufacturer values 
with open("manufacturer_data/eval_results.csv", "w") as out_csv: 
    csv_writer = csv.writer(out_csv)
    ##### Write your code below #####
    csv_writer.writerow([])