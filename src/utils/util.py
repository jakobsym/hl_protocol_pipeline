from typing import Dict, Optional, List

def merge_dict(d1: Optional[dict], d2: Optional[dict]) -> dict:
    
    items1 = d1.get('items', [])
    items2 = d2.get('items', [])
    
    merged_items = {}
    for item in items1 + items2:
        if item:
            address = item.get('address')
            if address:
                if address not in merged_items:
                    merged_items[address] = item.copy()
                else:
                    # merge overlapping fields with preference to d2
                    for key, value in item.items():
                        if value is not None and merged_items[address].get(key) is None:
                            merged_items[address][key] = value
    
    
    merged_items_list = list(merged_items.values())
    
    result = d1.copy()
    result.update(d2)
    result['items'] = merged_items_list
    
    return result
