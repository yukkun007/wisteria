{%- if books_len > 0 -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　期限切れ{{ xdays }}日以内：{{ books_len }}冊
───────────
{% else -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　期限切れ{{ xdays }}日以内：0冊
───────────
{% endif -%}
