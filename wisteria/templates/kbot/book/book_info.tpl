━━━━━━━━━━━
􀁬{{ book.title }}
━━━━━━━━━━━
■著：{{ book.author }}
■価格：￥{{ book.price }}
■ISBN：{{ book.isbn }}

{{ book.caption }}

───────────
􀁌図書館
───────────
予約: https://{{ my_server_name }}/kbot/library/reserve?book_id={{ book_id }}

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
