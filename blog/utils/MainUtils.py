from flask import request
from flask_paginate import Pagination, get_page_parameter


def Paginate(number_of_recoreds, model_name, query):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = number_of_recoreds
    query_list = model_name.query.order_by(query)
    total = query_list.count()
    pagination = Pagination(page=page, total=total, per_page=per_page)
    offset = (page - 1) * per_page
    query_per_page = query_list.limit(per_page).offset(offset)
    return pagination, query_per_page
