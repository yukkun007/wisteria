━━━━━━━━━━━
􀁬{{ book.title }}
━━━━━━━━━━━
■著：{{ book.author }}
■価格：￥{{ book.price }}
■発売日：{{ book.sales_date }}
■ISBN：{{ book.isbn }}

{{ book.caption }}

───────────
􀁌図書館
───────────
予約: https://{{ my_server_name }}/kbot/library/reserve?book_id={{ book.id }}

{% for key, value in book.libkey.items() -%}
{% if value == '貸出可' -%}
 􀂥{{ key }}: {{ value }}
{% else -%}
 􀂦{{ key }}: {{ value }}
{% endif -%}
{% endfor %}

───────────
􀁐楽天ブックス
───────────
購入: {{ book.url }}
