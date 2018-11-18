{%- if user.rental_books.len > 0 %}
───────────
{% if user.rental_books.filter_setting.is_type_none -%}
􀂏{{ user.name }}({{ user.id }})
　　　貸出：{{ user.rental_books.len }}冊
{%- elif user.rental_books.filter_setting.is_type_expired -%}
􀁽{{ user.name }}({{ user.id }})
　　　延滞：{{ user.rental_books.len }}冊
{%- elif user.rental_books.filter_setting.is_type_expire -%}
􀂏{{ user.name }}({{ user.id }})
　{{ user.rental_books.filter_setting.xdays }}日以内で延滞：{{ user.rental_books.len }}冊
{%- endif %}
───────────
{%- else %}
───────────
􀂏{{ user.name }}({{ user.id }})
{%- if user.rental_books.filter_setting.is_type_none %}
　　　貸出：0冊
{%- elif user.rental_books.filter_setting.is_type_expired %}
　　　延滞：0冊
{%- elif user.rental_books.filter_setting.is_type_expire %}
　{{ user.rental_books.filter_setting.xdays }}日以内で延滞：0冊
{%- endif %}
───────────
{% endif -%}
{%- for date, keyed_books in date_keyed_books_dict.items() %}
{% if keyed_books[0].is_expired() == True -%}􀂢{%- elif keyed_books[0].is_expire_in_xdays(2) == True -%}􀂤{%- else -%}􀀹{%- endif -%}{{ keyed_books[0].expire_date_text }}{{ keyed_books[0].get_expire_text_from_today() }}
{% for book in keyed_books -%}
 {%- if book.can_extend_period %}􀂥{%- else -%}􀂦{%- endif -%}{{ book.name }}
{% endfor -%}
{%- endfor -%}
