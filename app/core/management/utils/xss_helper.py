def sort_version(sort_list, reverse_order=False):
    """
    Sort a list of Terms or TermSet by version number
    """
    sort_list.sort(key=lambda item: int(item.version.split('.')
                   [2]), reverse=reverse_order)
    sort_list.sort(key=lambda item: int(item.version.split('.')
                   [1]), reverse=reverse_order)
    sort_list.sort(key=lambda item: int(item.version.split('.')
                   [0]), reverse=reverse_order)
    return sort_list
