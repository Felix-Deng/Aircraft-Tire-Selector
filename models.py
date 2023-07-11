class Tire: 
    """ This class stores all the specification of a tire along with common 
    calculations applied to the tire selection process. 
    """
    
    def __init__(self, M: float, N: float, D: float, R=False) -> None:
        """ When a Tire object is created, store all given key dimensions. 

        Args:
            M (float): _description_
            N (float): _description_
            D (float): _description_
            R (bool, optional): _description_. Defaults to False.
        """
        self.nominal_overall_diameter = M
        self.nominal_section_width = N
        self.rim_diameter = D
        self.is_radial = R
        ##### Add more parameters if needed (& update docstring) #####
        
    ##### Define more functions below if needed #######
    ##### to reach the max_load_capacity function #####
    
    
    
    def max_load_capacity(self) -> float: 
        """Calculate the maximum loading capacity of the tire.

        Returns:
            float: maximum loading capacity 
        """
        return 0.0 


if __name__ == "__main__": 
    ###### Test run this file to make sure the max loading capacity is printed ######
    tire = Tire() # Fill in the parameters required 
    print(tire.max_load_capacity())