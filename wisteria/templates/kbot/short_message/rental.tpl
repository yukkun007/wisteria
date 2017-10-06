{%- if books_len > 0 -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　　　貸出：{{ books_len }}冊
───────────
{% else -%}

───────────
􀂏{{ user.name }}({{ user.id }})
　　　貸出：0冊
───────────
{% endif -%}
