from django import template


register = template.Library()


@register.simple_tag
def task_filter_field(field):
    classes = ['form-select', 'mr-3', 'ml-2']
    if field.name == 'self_tasks':
        return field.as_widget(attrs={
            'class': 'form-check-input mr-3'
        })
    if not field.value():
        pass
    elif not field.errors:
        classes.append('is-valid')
    else:
        classes.append('is-invalid')
    return field.as_widget(attrs={'class': ' '.join(classes)})
