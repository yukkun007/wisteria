<hr></hr>
{%- if books_len > 0 -%}
<h3>{{ user.name }}(ID:{{ user.id }})</h3>{{ user.name }}の借りた次の本は、返却期限まであと{{ xdays }}日を切りました。
{% else -%}
{{ user.name }}(ID:{{ user.id }})の借りてる本で返却期限まであと{{ xdays }}日を切った本はありません。
{% endif -%}
<p><b>{{ books_len }}冊</b></p>
