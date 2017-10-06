{%- if books_len > 0 -%}

───────────
􀂏{{ user.name }}({{ user.id }})
───────────
　期限切れ近し：{{ books_len }}冊
　期限切れまで：あと{{ xdays }}日
{% else -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　返却期限まであと{{ xdays }}日を切った本はありません。
───────────
{% endif -%}
