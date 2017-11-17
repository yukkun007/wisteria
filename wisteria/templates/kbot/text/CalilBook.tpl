
───────────
􀁌図書館
───────────
予約: {{ object.kbot_reserve_url }}{{ object.id }}

{% for key, value in object.libkey.items() -%}
{% if value == '貸出可' -%}
 􀂥{{ key }}: {{ value }}
{% else -%}
 􀂦{{ key }}: {{ value }}
{% endif -%}
{% endfor %}
