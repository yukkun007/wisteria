<hr></hr>
{% if books_len > 0 %}
<h3>{{ user.name }}(ID:{{ user.id }})</h3>{{ user.name }}の借りた次の本は、期限が切れています！
{% else %}
{{ user.name }}(ID:{{ user.id }})の借りてる本で期限切れの本はありません。
{% endif %}
<p><b>{{ books_len }}冊</b></p>
