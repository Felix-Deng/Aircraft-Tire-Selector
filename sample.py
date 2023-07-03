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

