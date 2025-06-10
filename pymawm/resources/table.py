def tabularize(data_list, max_width=30):
    '''converts filtered data into a table, columns are max of 30 chars wide'''
    ##get all keys
    tab_keys = set()
    rows = []
    for data in data_list:
        tab_keys.update(set(data.keys()))
    ##add to row based on key
    for data in data_list:
        row = []
        for key in tab_keys:
            if key not in data:
                row.append('')
            else:
                row.append(str(data[key]))
        rows.append(row)
    ##combine and calculate widths
    table = rows
    col_widths = []
    for i, row in enumerate(table):
        if i < 1:
            for col in row:
                col_widths.append(len(col))
        else:
            for j, col in enumerate(row):
                if len(col) > col_widths[j]:
                    col_widths[j] = len(col)
    heading = [r for i, r in enumerate(tab_keys)] 
    print('\033[4m', *['|' + r.center(col_widths[i])[:max_width] + '| ' for i, r in enumerate(tab_keys)], '\033[0m')
    for row in table:
        print(*[' |' + r.center(col_widths[i])[:max_width] + '|' for i, r in enumerate(row)])
    return [heading] + table