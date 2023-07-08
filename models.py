class Tire: 
    """ This class stores all the specification of a tire along with common 
    calculations applied to the tire selection process. 
    """
    
    def __init__(self, M: float, N: float, D: float, R=False) -> None:
        """The Three Part Nomenclature of aircraft tires is given in 
        M x N - D or M x N R D. 

        Args:
            M (float): nominal overall diameter (inch)
            N (float): nominal section width (inch)
            D (float): rim diameter (inch)
            R (bool, optional): is the tire radial? Bias otherwise for "-". 
                Defaults to False.
        """
        self.nominal_overall_diameter = M
        self.nominal_section_width = N
        self.rim_diameter = D
        self.is_radial = R
