





DEFAULT_PAGE_SIZE = 3

def _get_pagination_params(page: int, page_size: int ):
    if page < 0:
        page = 0
    if page_size <= 0:
        page_size = DEFAULT_PAGE_SIZE

    offset = page * page_size
    return offset, page_size



# The following methods modify a query to select the specific elements belonging to a page of the query results.
# For pagination to make sense, some order must be established, but sometimes order may already exist. So two methods were
# created to both avoid possible duplication of ordering computations


def paginate_query(query, page: int, page_size: int = DEFAULT_PAGE_SIZE):
    offset, max_size = _get_pagination_params(page, page_size)
    return query.offset(offset).limit(max_size)

def order_and_paginate_query(query,  FieldForOrdering, page: int, page_size: int = DEFAULT_PAGE_SIZE):
    offset, max_size = _get_pagination_params(page, page_size)
    return (query.order_by(FieldForOrdering)
                .offset(offset).limit(max_size))




