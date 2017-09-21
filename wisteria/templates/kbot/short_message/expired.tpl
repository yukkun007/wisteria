{% if books_len > 0 %}
{{ user.name }}(ID:{{ user.id }})の借りた次の本({{ books_len }}冊)は、期限が切れています！
{% else %}
{{ user.name }}(ID:{{ user.id }})の借りてる本で期限切れの本はありません。
{% endif %}
