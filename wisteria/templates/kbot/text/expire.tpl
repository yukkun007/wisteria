{%- if books_len > 0 -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　{{ xdays }}日以内で延滞：{{ books_len }}冊
───────────
{% else -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　{{ xdays }}日以内で延滞：0冊
───────────
{% endif -%}
