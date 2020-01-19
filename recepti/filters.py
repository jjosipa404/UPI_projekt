import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):

    #CHOICES = {
        #('ascending', 'Uzlazno (A - Z)'),
        #('descending', 'Silazno (Z - A)')
    #}

    #ordering = django_filters.ChoiceFilter(label='Oredring', choices = CHOICES, method = 'filter_by_order')
    class Meta:
        model = Post
        fields = {
             'naslov': ['icontains'],
         }


   # def filter_by_order(self, queryset, name, value):
       # expression = 'created' if value == 'ascending' else '-created'
       # return queryset.order_by(expression)

class PostFilter(django_filters.FilterSet):
    class Meta:
        model=Post
        fields={
            'naslov':['icontains'],
        }

