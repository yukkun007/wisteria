{%- if books_len > 0 -%}
{{ user.name }}(ID:{{ user.id }})は{{ books_len }}冊借りています。
{% else -%}
{{ user.name }}(ID:{{ user.id }})の借りてる本はありません。
{% endif -%}
