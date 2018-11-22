{%- for book in books.list %}
􀁬{{ book.title }}
■著者：{{ book.author }}
■出版社：{{ book.publisher }}
■出版日：{{ book.publish_date }}

{% endfor -%}
