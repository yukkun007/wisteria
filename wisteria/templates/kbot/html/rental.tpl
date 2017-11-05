<hr></hr>
{%- if books_len > 0 -%}
<h3>{{ user.name }}(ID:{{ user.id }})</h3>{{ user.name }}の借りてる本です。
{% else -%}
{{ user.name }}(ID:{{ user.id }})の借りてる本はありません。
{% endif -%}
<p><b>{{ books_len }}冊</b></p>
