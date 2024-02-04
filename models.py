import inspect
from typing import List, Optional
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
        self.Dm: float = kwargs.get("Dm", (self.DoMax + self.DoMin) / 2) # mean tire diameter 
        self.WMax: float = kwargs.get('WMax', 0)
        self.WMin: float = kwargs.get('WMin', 0)
        self.Wm: float = kwargs.get("Wm", (self.WMax + self.WMin) / 2) # mean overall tire width 
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
        
    def __str__(self) -> str:
        return f'''{'*'*20}
Tire Design Parameters:
- Dm: {self.Dm} in
- Wm: {self.Wm} in
- D: {self.D} in
- DF: {self.DF} in
- PR: {self.PR} in
Tire Performance: 
- Lm (analytical): {self.max_load_capacity(exact=True)} lbs
- Mass of Inflation Medium: {round(self.inflation_medium_mass(), 4)} kg
- Speed Index: {self.SI} mph
- Aspect Ratio: {self.aspect_ratio()}
{'*'*20}'''
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tire): 
            attr_self = [
                a[1] for a in inspect.getmembers(self) 
                if not a[0].startswith("__") and not inspect.ismethod(a[1])
            ]
            attr_other = [
                a[1] for a in inspect.getmembers(other) 
                if not a[0].startswith("__") and not inspect.ismethod(a[1])
            ]
            for i, item in enumerate(attr_self): 
                if not item == attr_other[i]: 
                    return False 
            return True 
        else: 
            return False 
        
    def get_key_dim(self) -> List[float]: 
        """Return the key dimensions of the tire 

        Returns:
            List[float]: ['PR', 'Dm', 'Wm', 'D', 'DF'] 
        """
        return [self.PR, self.Dm, self.Wm, self.D, self.DF] 
    
    def aspect_ratio(self) -> Optional[float]: 
        """Return the aspect ratio of the tire 

        Returns:
            Optional[float]: aspect ratio
        """
        try: 
            return (self.Dm - self.D) / 2 / self.Wm
        except ZeroDivisionError:
            return None 

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

    def is_mech_feasible(self, model="walter", N=0, n_ply=0, break_load=338.0) -> bool: 
        """Compare if the required load exceeds the designed brake load of the material. 
        
        Args:
            model (str, optional): type of model in {"walter", "netting"}. 
                Defaults to "walter". 
            N (int, optional): number of cords per ply. Defaults to 0 when 
                tested maximum allowable number from manufacturer is used.
            n_ply (int, optional): number of plies. Defaults to 0 when 
                half of ply rating is used. 
            break_load (float, optional): material designed breaking load in N. 
                Defaults to 338.0.

        Returns:
            bool: if the tire is mechanically feasible based on cord strength 
        """
        if model == "walter": 
            t = self.cord_tension_walter(N=N, n_ply=n_ply)
        elif model == "netting": 
            t = self.cord_tension_netting(N=N, n_ply=n_ply)
        else: 
            raise ValueError("Unsupported model type. Currently only support {\"walter\", \"netting\"}")
        
        if t < break_load: # comparison made in N 
            return True 
        else: 
            return False 
    
    def cord_tension_netting(self, N=0, n_ply=0, alpha=30.0, phi=90.0) -> float: 
        """Calculate the tension each tire reinforcement cord needs to sustain using 
        the netting model. 

        $t = pi / P / N * ({\rho}^2 - {\rho_m}^2) / \sin(\alpha) / \sin(\phi)$
        
        Args:
            N (int, optional): number of cords per ply. Defaults to 0 when 
                tested maximum allowable number from manufacturer is used.
            n_ply (int, optional): number of plies. Defaults to 0 when 
                half of ply rating is used. 
            alpha (float, optional): cord angle in degrees. Defaults to 30.0.
            phi (float, optional): angle between $\Delta s$ tangent line and 
                the tire meridian line in degree. Defaults to 90.0.

        Returns:
            float: fiber tension in N 
        """
        if not n_ply: 
            n_ply = np.ceil(self.PR / 8)
        if not N: 
            N = 1540
            
        t = np.pi * self.inflation_pressure() / (N * n_ply) * (
            (self.Dm/2) ** 2 - (self.Dm/2 - (self.Dm - self.D)/4) ** 2
        ) / np.sin(alpha * constants.degree) / np.sin(phi * constants.degree) 
        
        return t * constants.lbf
    
    def cord_tension_walter(self, N=0, n_ply=0, beta_c=30.0, m_1= 71e-6, rho=0.9, beta_s=45.00) -> float: 
        """Calculate the tension each tire reinforcement cord needs to sustain using 
        the Walter model, which combines the netting model and the shell model to 
        include both static loading and centrifugal force from dynamic tire rotation. 

        Args:
            N (int, optional): number of cords per ply. Defaults to 0 when 
                tested maximum allowable number from manufacturer is used.
            n_ply (int, optional): actual number of plies used. Defaults to 0.
            beta_c (float, optional): angle (in degree) between the cord and a meridian 
                plane at the crown of the tire. Defaults to 30.0.
            m_1 (float, optional): average (constant) mass of rubber and cord per unit area 
                of tire surface in the interval between the crown and shoulder (in lb.sec^2/in^3). 
                Defaults to 71e-6. 
            rho (float, optional): dimensionless radial coordinate (r/r_c). Defaults to 0.9.
            beta_s (float, optional): angle (in degree) between the cord and a meridian 
                plane at the shoulder. Defaults to 45.00.

        Returns:
            float: fiber tension in N 
        """
        def psi(_rho: float, _beta_c: float) -> float: 
            """
            Args:
                _rho (float): rho in parent function 
                _beta_c (float): beta_c in parent function (in radian)

            Returns:
                float: psi(rho)
            """
            return (
                2 * _rho * (1 - _rho**2 * np.sin(_beta_c)**2) ** (2/3) - 
                _rho * (1 - _rho**2 * np.sin(_beta_c)**2) ** (1/2) - 
                np.arcsin(_rho * np.sin(_beta_c)) / np.sin(_beta_c)
            ) / (4 * np.sin(_beta_c)**2)
        
        if not n_ply: 
            n_ply = np.ceil(self.PR / 8)
        if not N: 
            N = 1360 
        
        beta_c *= constants.degree
        beta_s *= constants.degree
        r_c = self.Dm / 2 # radial distance from axis of revolution to crown 
        r_w = self.Dm / 2 - (self.Dm - self.D) / 4 # radial distance from axis of revolution to widest part of tire meridian 
        rho_w = r_w / r_c 
        omega = self.SI * (constants.mile / constants.inch / constants.hour) / r_c # angular velocity 
        Omega = r_c * (omega) ** 2 / self.inflation_pressure() # geometry and load parameter 
        
        t = np.pi * self.inflation_pressure() * (r_c ** 2) * (
            (1 - rho_w**2) * np.cos(beta_c) + m_1 * Omega * (psi(rho, beta_c) - psi(1, beta_c))
        ) / (
            N * n_ply * (1 - rho ** 2 * (np.sin(beta_s) ** 2))
        )
        return t * constants.lbf


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
        + f'With calculated pressure: {round(tire.inflation_medium_mass(P_gas=tire.IP), 2)} kg\n'\
        + '\nReinforcement cord tension:\n'\
        + f'With Netting model: {tire.cord_tension_netting()} N\n'\
        + f'With Walter model: {tire.cord_tension_walter()} N'
    )
    