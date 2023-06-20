from rest_framework.fields import Field
#это конечно можно было и не делать , просто эксперементирую, учусь)

class ReadOnlyMixin(Field):

    def __new__(cls, *args, **kwargs):
        setattr(
            cls.Meta,
            "read_only_fields",
            [f.name for f in cls.Meta.model._meta.get_fields()],
        )
        return super(ReadOnlyMixin, cls).__new__(cls, *args, **kwargs)
