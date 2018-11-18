<hr></hr>
{%- if user.rental_books.len > 0 -%}
<h3>{{ user.name }}(ID:{{ user.id }})</h3>
{% if user.rental_books.filter_setting.is_type_none -%}
{{ user.name }}の借りてる本です。
{%- elif user.rental_books.filter_setting.is_type_expired -%}
{{ user.name }}の借りた次の本は、期限が切れています！
{%- elif user.rental_books.filter_setting.is_type_expire -%}
{{ user.name }}の借りた次の本は、返却期限まであと{{ user.rental_books.filter_setting.xdays }}日を切りました。
{% endif -%}
{% else -%}
{{ user.name }}(ID:{{ user.id }})
{%- if user.rental_books.filter_setting.is_type_none -%}
の借りてる本はありません。
{%- elif user.rental_books.filter_setting.is_type_expired -%}
の借りてる本で期限切れの本はありません。
{%- elif user.rental_books.filter_setting.is_type_expire -%}
の借りてる本で返却期限まであと{{ user.rental_books.filter_setting.xdays }}日を切った本はありません。
{% endif -%}
{% endif -%}
<p><b>{{ user.rental_books.len }}冊</b></p>

<div>
<table width="95%" border="1" align="center" cellspacing="0" cellpadding="2">
<tr><th bgcolor="#ff7f50" width="60%">本</th><th bgcolor="#ff7f50">返却期限日</th></tr>
{% for date, keyed_books in date_keyed_books_dict.items() -%}
{% for book in keyed_books -%}
<tr><td>{{ book.name }}</td><td>{{ book.expire_date_text }}</td></tr>
{% endfor -%}
{% endfor -%}
</table>
</div>
<br>

