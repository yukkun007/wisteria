{%- if user.reserved_books.len > 0 %}
───────────
{% if is_prepared %}􀁹{% else %}􀂐{% endif %}{{ user.name }}({{ user.id }})
　　　対象：{{ user.reserved_books.len }}冊
───────────
{%- else %}
───────────
􀂐{{ user.name }}({{ user.id }})
　　　対象：0冊
───────────
{%- endif -%}
{% for book in user.reserved_books.list %}
􀁬{{ book.title }}
{% if book.is_prepared == True %}􀁠{% elif book.is_dereverd == True %}􀁉{% else %}■{% endif %}状況：{{ book.status }}
■順位：{% if book.is_prepared == True %}-{% elif book.is_dereverd == True %}-{% else %}{{ book.order }}{% endif %}
■取置期限日：{{ book.torioki_date }}

{% endfor -%}

