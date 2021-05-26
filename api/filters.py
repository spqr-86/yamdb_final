import django_filters


class TitleFilterBackend(django_filters.rest_framework.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        if name:
            return queryset.filter(name__contains=name)

        return super(TitleFilterBackend, self).filter_queryset(
            request,
            queryset,
            view
        )
