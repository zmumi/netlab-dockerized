initial_nodes = [{% for node in nodes %}{
    properties: {
        {% for prop, val in node.items %}
        {% if prop != 'id' %}
        {{prop}}:"{{val}}",
        {% endif %}
        {% endfor %}
    },
    id: "{{node.id}}",
    label: "{{node.id}}"
},{% endfor %}]


initial_edges = [{% for edge in edges %}{
    properties: {
        {% for prop, val in edge.items %}
        {% if prop != 'id' and prop != 'from' and prop != 'to' %}
        {{prop}}:"{{val}}",
        {% endif %}
        {% endfor %}
    },
    id: "{{edge.id}}",
    from: "{{edge.from}}",
    to: "{{edge.to}}"
},{% endfor %}]
