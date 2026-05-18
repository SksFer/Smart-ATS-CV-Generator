# {{ personal.nombre }}
Teléfono: {{ personal.telefono }} | LinkedIn: {{ personal.linkedin }}

## Perfil Profesional
{{ perfil }}

## Proyectos

{% for proyecto in proyectos %}
**{{ proyecto.titulo }}** | *{{ proyecto.fecha }}*
*{{ proyecto.descripcion }}*
{% for bullet in proyecto.bullets %}
- {{ bullet }}
{% endfor %}
{% endfor %}

## Habilidades Técnicas

{% for habilidad in habilidades %}
- {{ habilidad.texto }}
{% endfor %}

## Educación

{% for edu in educacion %}
**{{ edu.institucion }}** | *{{ edu.fecha }}*
{{ edu.titulo }}
- {{ edu.descripcion }}
{% endfor %}

## Experiencia Adicional

{% for exp in extra %}
**{{ exp.titulo }}**, *{{ exp.institucion }}* | *{{ exp.fecha }}*
{% for bullet in exp.bullets %}
- {{ bullet }}
{% endfor %}
{% endfor %}