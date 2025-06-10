import logging
logger = logging.getLogger(__name__)


def handle_sort(sort):
    # converts string into list then dict by handling , or space separated
    # if sort only has fieldname specified, append 'asc' by default
    if type(sort) == dict:
        return sort
    elif type(sort) == str and ',' in sort: # comma should mean multi sort: "OrderId asc, OrderType desc"
        sort = sort.split(',')
        logger.debug(f"parsing multi-sort: {sort}")
        out_sort = []
        for s in sort:
            s = s.split()
            if len(s) == 1:
                s.append('asc')
            out_sort.append({
                "attribute": s[0].strip(),
                "direction": s[1].strip()
            })
        return out_sort
    elif type(sort) == str:
        sort = sort.split()
    if len(sort) == 1:
        sort.append('asc')
    sort = {
            "attribute": sort[0].strip(),
            "direction": sort[1].strip()
        }
    return sort

def handle_template(template): 
    #turns list or string into dict
    if type(template) == list:
        out_template = {key:None for key in template}
    elif type(template) == str:
        template = template.split(',')
        out_template = {key.strip():None for key in template}
    return template

def parse(page='', query='', size='', sort='', template='', limit='', offset='', sorted=''):
    if sort != '':
        sort = handle_sort(sort)
    if template != '':
        template=handle_template(template)
    query = {
        'Page': page,
        'Query': query,
        'Size': size,
        'Sort': sort,
        'Template': template,
        'Limit': limit,
        'Offset': offset,
        'Sorted': sorted
    }
    query = {k:v for k, v in query.items() if v != ''} #clearing empty values 
    logger.debug(f"parsed query: {query}")
    return query