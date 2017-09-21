<div>
<table width="95%" border="1" align="center" cellspacing="0" cellpadding="2">
<tr><th bgcolor="#ff7f50" width="60%">本</th><th bgcolor="#ff7f50">返却期限日</th></tr>
{% for book in books_org -%}
<tr><td>{{ book.name }}</td><td>{{ book.expire_date_text }}</td></tr>
{% endfor -%}
</table>
</div>
<br>

