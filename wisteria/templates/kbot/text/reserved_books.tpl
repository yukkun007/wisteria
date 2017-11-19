
───────────
{% if is_prepared %}􀁹{% else %}􀂐{% endif %}{{ books.user.name }}(ID:{{ books.user.id }})
───────────
{% for book in books.list -%}
􀁬{{ book.title }}
{% if book.is_prepared == True %}􀁠{% else %}■{% endif %}状況：{{ book.status }}
■順位：{{ book.order }}
■区分：{{ book.kind }}
■予約日：{{ book.yoyaku_date }}
■取置期限日：{{ book.torioki_date }}

{% endfor -%}

