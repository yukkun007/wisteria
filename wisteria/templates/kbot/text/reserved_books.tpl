{%- if books.len > 0 %}
───────────
{% if is_prepared %}􀁹{% else %}􀂐{% endif %}{{ books.user.name }}({{ books.user.id }})
　　　対象：{{ books.len }}冊
───────────
{%- else %}
───────────
􀂐{{ books.user.name }}({{ books.user.id }})
　　　対象：0冊
───────────
{%- endif -%}
{% for book in books.list %}
􀁬{{ book.title }}
{% if book.is_prepared == True %}􀁠{% elif book.is_dereverd == True %}􀁉{% else %}■{% endif %}状況：{{ book.status }}
■順位：{{ book.order }}
■区分：{{ book.kind }}
■予約日：{{ book.yoyaku_date }}
■取置期限日：{{ book.torioki_date }}

{% endfor -%}

