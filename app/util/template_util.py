from flask import render_template_string


class Pagination:
    def format_pagination(page_no, page_size, count):
        pagination_template = 'templates/web/w1/pagination.json'

        pagination = {
            'page_no': page_no,
            'page_size': page_size,
            'count': count
        }

        return render_template_string(open(pagination_template).read(), pagination=pagination)