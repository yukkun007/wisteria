{% if books_len > 0 -%}

───────────
􀁽{{ user.name }}({{ user.id }})
　期限切れ：{{ books_len }}冊
───────────
{% else -%}

───────────
􀁽{{ user.name }}({{ user.id }})
　期限切れ：0冊
───────────
{% endif -%}
