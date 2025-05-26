from typing import Dict

def merge_dict(d1: Dict,d2: Dict) -> Dict:
    new_dict = d1 | d2
    if not new_dict:
        return {d1, d2}
    return new_dict

