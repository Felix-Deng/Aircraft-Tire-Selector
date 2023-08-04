import numpy as np 
from scipy import constants 

class Tire: 
    """ This class stores all the specification of a tire along with common 
    calculations applied to the tire selection process. 
    """
    
    def __init__(self, **kwargs) -> None:
        """Initiate a Tire object to store all parameters of an aircraft tire. 
        
        kwargs include all parameters given from manufacturer's databook. 
        """
        # Tire Descriptions
        self.Pre: str = kwargs.get('Pre', '')
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
        self.Dm = (self.DoMax + self.DoMin) / 2     # mean tire diameter 
        self.WMax: float = kwargs.get('WMax', 0)
        self.WMin: float = kwargs.get('WMin', 0)
        self.Wm = (self.WMax + self.WMin) / 2       # mean overall tire width 
        self.DsMax: float = kwargs.get('DsMax', 0)
        self.WsMax: float = kwargs.get('WsMax', 0)
        
        # Aspect Ratio
        self.AR: float = kwargs.get('AR', 0)
        
        #Static Loading Radius (inches)
        self.LR_RL: float = kwargs.get('LR_RL', 0)
        self.LR_BL: float = kwargs.get('LR_BL', 0)
        
        # Rim Description (inches)
        self.A: float = kwargs.get('A', 0)
        self.RD: float = kwargs.get('RD', 0)
        self.FH: float = kwargs.get('FH', 0)
        self.G: float = kwargs.get('G', 0)
        self.DF: float = kwargs.get('DF', 0)
        
        # Qualification Standard
        self.QS: str = kwargs.get('QS', '')
        
        # Check for missing values 
        if not self.D:
            self.D = self.RD
        if not self.DF: 
            self.DF = self.D + 2 * self.FH
        
        self.Lr = self.Dm/self.D # lift ratio

    def max_load_capacity(self, exact=False) -> float: 
        """
        Args:
            exact (bool, optional): should the exact load be returned? Defaults to False.

        Returns:
            float: maximum loading capacity of the tire (Lm) in lbs; 
                returned value rounded to the nearest 25 pounds if not exact. 
        """
        Lm = self.ground_contact_area() * (
            self.pressure_index() + self.load_supporting_capability()
        ) 
        if exact: 
            return Lm 
        else: 
            return np.round(Lm / 25) * 25 
    
    def ground_contact_area(self, b=0.32) -> float:
        """
        Args:
            b (float, optional): fractional tire deflection. 
                Defaults to 0.32 for type VII tires.

        Returns:
            float: ground contact area of the tire (Ad) in inch^2 
        """
        d = b * (self.Dm - self.DF)/2  # actual deflection of the tire 
        return 0.77 * constants.pi * d * np.sqrt((self.Dm - d) * (self.Wm - d))
    
    def pressure_index(self) -> float:
        """
        Returns:
            float: pressure index of the tire (P)
        """
        Re = self.ratio_of_ends_per_inch()
        Ne = self.PR - 0.4
        T0 = 4.4  # 4 for type III tires, 4.4 otherwise
        a = (self.Dm - self.D)/4
        Q = 2.5 + self.D / (2 * self.Dm)
        S = a * Q
        F0 = (
            -1.623104e-7 * self.D**5 \
            + 1.463062e-5 * self.D**4 \
            - 5.607522e-4 * self.D**3 \
            + 0.01288401 * self.D**2 \
            - 0.197904 * self.D \
            + 2.567982
        )
        return (40 * Re * T0 * Ne) / (S * F0)
    
    def ratio_of_ends_per_inch(self) -> float:
        """
        Returns:
            float: ratio of ends per inch of the tire (Re)
        """
        if 1.5 < self.Lr < 2.2:
            return 1.475 - 0.331 * self.Lr
        elif 2.2 <= self.Lr < 5:
            return (
                -0.007651 * self.Lr**5 \
                + 0.14362 * self.Lr**4 \
                - 1.0668308 * self.Lr**3 \
                + 3.9519228 * self.Lr**2 \
                - 7.4168297 * self.Lr \
                + 6.3261135
            )
        else:
            # raise ValueError("Lr value is outside the defined range.")
            if self.Lr <= 1.5:
                return 1.475 - 0.331 * self.Lr
            else:
                return (
                    -0.007651 * 5**5 \
                    + 0.14362 * 5**4 \
                    - 1.0668308 * 5**3 \
                    + 3.9519228 * 5**2 \
                    - 7.4168297 * 5 \
                    + 6.3261135
                )
    
    def load_supporting_capability(self) -> float:
        """
        Returns:
            float: load supporting capability of the tire carcass 
                in units of equivalent pressure (Pc)
        """
        # assume the mean cross section == mean tire width 
        if self.Wm < 5.5:
            return self.PR
        else:
            return (10.4 * self.PR ** 2) / self.Wm ** 2
        
    def inflation_medium_mass(self, P_gas=0.0, P_amb=14.7, T=298.15, M_gas=28.0134) -> float: 
        """
        Args:
            P_gas (float, optional): tire gas inflation pressure in psi. 
                Defaults to 0.0 to calculate using equations.
            P_amb (float, optional): ambient pressure in psi. 
                Defaults to standard atmospheric pressure 14.7 psi (101325 Pa).
            T (float, optional): absolute temperature in Kelvin. 
                Defaults to 298.15 K (25 degree celsius) for standard ambient temperature.
            M_gas (float, optional): molar mass of the inflation gas in g/mol. 
                Defaults to 28.0134 g/mol for nitrogen. 
                For air, M_gas = 29 g/mol. 

        Returns:
            float: mass of the inflation medium (gas) of the tire (m) in kg 
        """
        # Pressure 
        if not P_gas: 
            P_gas = self.inflation_pressure() 
        P_abs = (P_gas + P_amb) * constants.psi 
        
        # Volume 
        H = (self.Dm - self.D) / 2 # section height 
        V = constants.pi**2 * self.Wm * H * (self.D + H) / 4 * constants.inch**3
        
        return P_abs * V * M_gas / constants.R / T / 1000 
    
    def inflation_pressure(self) -> float: 
        """
        Returns:
            float: indicator inflation pressure of the tire in psi. 
        """
        Pc = self.load_supporting_capability() 
        
        if self.Pre == "B" or self.Pre == "H" or (self.SI and self.SI <= 160): # 35% tire deflection 
            b = 0.35 
            P = self.max_load_capacity() / (b + 0.45) / self.ground_contact_area(b=b) - Pc
        else: # 32% tire deflection 
            P = self.pressure_index() 
        
        if P > 100: 
            X = 0.5 
        else: 
            X = 0.01 * P - 0.5 
        
        return P + X * Pc + 3 


if __name__ == "__main__": 
    # Test run the max loading capacity calculation 
    tire = Tire(
        Pre='', M=21, N=7.25, D=10, PR=10, SI=210, Lm=5150, IP=135, BL=15450, DoMax=21.25, DoMin=20.60,
        WMax=7.20, WMin=6.80, DsMax=19.25, WsMax=6.35, AR=0.78, LR_RL=9, LR_BL=6.8, A=5.50, RD=10,
        FH=1, G=1.4, DF=12, QS='TSO-C62'
    )
    print(
        'Maximum load capacity of the tire:\n'\
        + f'From databook: {tire.Lm} lbs\n'\
        + f'From calculation (rounded): {tire.max_load_capacity()} lbs\n'\
        + f'From calculation (exact): {round(tire.max_load_capacity(exact=True), 2)} lbs\n'\
        + '\nInflation pressure of the tire:\n'\
        + f'From databook: {tire.IP} psi\n'\
        + f'From calculation: {round(tire.inflation_pressure(), 2)} psi\n'\
        + '\nMass of tire\'s inflation medium:\n'\
        + f'With databook pressure: {round(tire.inflation_medium_mass(), 2)} kg\n'\
        + f'With calculated pressure: {round(tire.inflation_medium_mass(P_gas=tire.IP), 2)} kg'
    )