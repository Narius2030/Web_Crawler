def data_processing(data_info):
    """Processing data before insert into table

    Args:
        data_info (list): list of movie items

    Returns:
        list: list of movie items after processing
    """    
    for items in data_info:
        for key in items:
            items[key] = items[key].replace("'", "")
    
    return data_info