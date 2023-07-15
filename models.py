import math

class Tire: 
    """ This class stores all the specification of a tire along with common 
    calculations applied to the tire selection process. 
    """
    
    def __init__(self, **kwargs) -> None:
        
        self.Pre: str = kwargs.get('Pre', 0)
        
        # Tire Descriptions
        self.M: float = kwargs.get('M', 0)
        self.N: float = kwargs.get('N', 0)
        self.D: float = kwargs.get('D', 0)
        self.PR: float = kwargs.get('PR', 0)
        self.SI: float = kwargs.get('SI', 0)
        
        # Application Rating
        self.Lm: float = kwargs.get('Lm', 0)
        self.IP: float = kwargs.get('IP', 0)
        self.BL: float = kwargs.get('BL', 0)
        
        # Inflated Tire Dimensions (inches)
        self.DoMax: float = kwargs.get('DoMax', 0)
        self.DoMin: float = kwargs.get('DoMin', 0)
        self.WMax: float = kwargs.get('WMax', 0)
        self.WMin: float = kwargs.get('WMin', 0)
        self.DsMax: float = kwargs.get('DsMax', 0)
        self.WsMax: float = kwargs.get('WsMax', 0)
        
        # Aspect Ratio
        self.AR: float = kwargs.get('AR', 0)
        
        #Static Loading Radius (inches)
        self.LR_RL: float = kwargs.get('LR_RL', 0)
        self.LR_BL: float = kwargs.get('LR_BL', 0)
        
        # Rim Description (inches)
        self.A: float = kwargs.get('A', 0)
        self.D2: float = kwargs.get('D2', 0)                # specified rim diameter
        self.FH: float = kwargs.get('FH', 0)
        self.G: float = kwargs.get('G', 0)
        self.DF: float = kwargs.get('DF', 0)                # outer flange diameter
        
        # Qualification Standard
        self.QS: str = kwargs.get('QS', 0)

    def max_load_capacity_calc(self) -> float: 
        """Calculate the maximum loading capacity of the tire.

        Returns:
            float: maximum loading capacity 
        """
        
        Ad = self.ground_contact_area_calc()                # ground contact area at d in in^2
        P = self.pressure_index_calc()                      # pressure index
        Pc = self.load_supporting_capability_calc()         # load supporting capability of the tire carcass in units of equivalent pressure
        
        # print(f'{Ad},    {P},    {Pc}')
        Lm = Ad * (P + Pc)                                  # maximum load capacity in lbs
        Lm = round(Lm / 25) * 25
    
        return Lm
    
    def ground_contact_area_calc(self) -> float:
        """Calculate the ground contact area of the tire.

        Returns:
            float: ground contact area (Ad)
        """
        d = self.actual_deflection_calc()       # actual deflection
        Dm = (self.DoMax + self.DoMin)/2        # mean tire diameter
        Wm = (self.WMax + self.WMin)/2          # mean overall tire width
        Ad = 0.77 * math.pi * d * math.sqrt((Dm - d) * (Wm - d))
        
        return Ad
    
    def actual_deflection_calc(self) -> float:
        """Calculate the actual deflection of the tire.

        Returns:
            float: actual deflection (d)
        """
        
        Dm = (self.DoMax + self.DoMin)/2        # mean tire diameter
        b = 0.32                                # fractional tire deflection, see Table 1
        d = b * (Dm - self.DF)/2    

        return d
    
    def pressure_index_calc(self) -> float:
        """Calculate the pressure index of the tire.

        Returns:
            float: pressure index (p)
        """
        
        # ratio of ends per inch
        Re = self.ratio_of_ends_per_inch_calc()
        
        # constants
        T0 = 4.4                 # 4 for type III tires and 4.4 for all other tires, since we only consider type III tire, 4.4 used for calculation
        Ne = self.PR - 0.4
        
        Dm = (self.DoMax + self.DoMin)/2        # mean tire diameter
        a = (Dm - self.D)/4
        Q = 2.5 + self.D/(2 * Dm)
        S = a * Q
        
        # operating factor
        F0 = (-1.623104 * 10 ** (-7) * self.D ** 5) + (1.463062 * 10 ** (-5) * self.D ** 4) - \
              (5.607522 * 10 ** (-4) * self.D ** 3) + (0.01288401 * self.D ** 2) - (0.197904 * self.D) + 2.567982 

        
        P = (40 * Re * T0 * Ne) / (S * F0)

        return P
    
    def ratio_of_ends_per_inch_calc(self) -> float:
        """Calculate the ratio of ends per inch of the tire.

        Returns:
            float: ratio of ends per inch (Re)
        """
        
        Dm = (self.DoMax + self.DoMin)/2        # mean tire diameter
        Lr = Dm/self.D                          # Lift Ratio
        
        if 1.5 < Lr < 2.2:
            Re = 1.475 - 0.331 * Lr
        elif 2.2 <= Lr < 5:
            Re = (-0.007651 * Lr ** 5) + (0.14362 * Lr ** 4) - (1.0668308 * Lr ** 3) + \
                   (3.9519228 * Lr ** 2) - (7.4168297 * Lr) + 6.3261135
        else:
            raise ValueError("Lr value is outside the defined range.")
        
        return Re
    
    def load_supporting_capability_calc(self) -> float:
        """Calculate the load supporting capability of the tire carcass in units of equivalent pressure.

        Returns:
            float: load supporting capability (Pc)
        """
        
        Dm = (self.DoMax + self.DoMin)/2        # mean tire diameter
        Wm = (self.WMax + self.WMin)/2          # mean overall tire width
        
        # assume the mean cross section == mean tire width for now, but it is probably not miss a length
        if Dm < 5.5:
            Pc = self.N
        else:
            Pc = (10.4 * self.PR ** 2) / Wm ** 2
        
        return Pc
        

############
# read csv
    @classmethod
    def from_row(cls, row):
        row_data = {}
        for key, value in zip(cls.header(), row):
            try:
                row_data[key] = float(value)
            except ValueError:
                row_data[key] = None  # Assign a default value if conversion fails
        return cls(**row_data)

    @staticmethod
    def header():
        return ['Pre','M', 'N', 'D', 'PR', 'SI', 'Lm', 'IP', 'BL', 'DoMax', 'DoMin', 'WMax', 'WMin', 'DsMax',
                'WsMax', 'AR', 'LR_RL', 'LR_BL', 'A', 'D2', 'FH', 'G', 'DF', 'QS']




'''
if __name__ == "__main__": 
    ###### Test run this file to make sure the max loading capacity is printed ######
    tire = Tire() # Fill in the parameters required 
    print(tire.max_load_capacity_calc())
'''