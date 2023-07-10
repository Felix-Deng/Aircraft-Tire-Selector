import csv 

with open("manufacturer_data/tire_data.csv") as data_csv: 
    csv_reader = csv.reader(data_csv)
    next(csv_reader)  # skip header row 
    for row in csv_reader: 
        """Column index: [
            'Pre', 'M', 'N', 'D', 'PR', 'SI', 'ML', 'IP', 'BL', 
            'DoMax', 'DoMin', 'WMax', 'WMin', 'DsMax', 'WsMax', 
            'AR', 'LR_RL', 'LR_BL', 'A', 'D', 'FH', 'G', 'DF', 'QS'
        ]
        """
        print(row)
        break 