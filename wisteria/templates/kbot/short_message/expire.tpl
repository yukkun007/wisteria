{%- if books_len > 0 -%}
{{ user.name }}(ID:{{ user.id }})の借りた次の本({{ books_len }}冊)は、返却期限まであと{{ xdays }}日を切りました。
{% else -%}
{{ user.name }}(ID:{{ user.id }})の借りてる本で返却期限まであと{{ xdays }}日を切った本はありません。
{% endif -%}
