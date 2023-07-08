from typing import Union, Optional 

def testing(number: int, string="") -> Optional[Union[int, str]]: 
    """_summary_

    Args:
        number (int): _description_
        string (str, optional): _description_. Defaults to "".

    Returns:
        Optional[Union[int, str]]: _description_
    """
    if number: 
        return number
    elif string: 
        return string 
    else: 
        return None 

class sample_cls: 
    """_summary_
    """
    attribute1 = 0 
    attribute2 = "Hi"
    
    def __init__(self, a: int) -> None:
        """_summary_

        Args:
            a (int): _description_
        """
        self.attribute1 = a
    
    def sample_method(self, add: bool) -> str: 
        """_summary_

        Args:
            add (bool): _description_

        Returns:
            str: _description_
        """
        if add: 
            return self.attribute2 + str(self.attribute1)
        else: 
            return str(self.attribute1)