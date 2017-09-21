===========
{% for date, books in date_keyed_books_dict.items() -%}
{% if books[0].is_expired() == True %}􀂢{% elif books[0].is_expire_in_xdays(2) == True -%}􀂤{% else -%}􀀹{% endif %}{{ books[0].expire_date_text }}{{ books[0].get_expire_text_from_today() }}
{% for book in books -%}
 {% if book.can_extend_period %}􀂥{% else -%}􀂦{% endif %}{{ book.name }}
{% endfor -%}
{% endfor -%}
===========


