import time
import hashlib
import random


from django.db.models import SlugField


def genHashKey():
    return '%s%s' % (time.time(), random.random())


class AutoMD5SlugField(SlugField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        populate_from = kwargs.pop('populate_from', None)
        if populate_from is None:
            self._populate_from = ''
        else:
            self._populate_from = populate_from

        self.hash_key = kwargs.pop('hash_key', time.time)
        super(AutoMD5SlugField, self).__init__(*args, **kwargs)

    def get_new_slug(self, model_instance, extra=''):
        slug_field = model_instance._meta.get_field(self.attname)

        if callable(self.hash_key):
            hash_key = self.hash_key()
        else:
            hash_key = self.hash_key
        temp = '%s%s%s' % (hash_key, getattr(model_instance, self._populate_from), extra)
        slug = hashlib.md5(temp.encode('utf-8')).hexdigest()
        slug_len = slug_field.max_length
        if slug_len:
            slug = slug[:slug_len]

        return slug

    def create_slug(self, model_instance, add):
        # get fields to populate from and slug field to set
        slug = getattr(model_instance, self.attname)
        if slug:
            # slugify the original field content and set next step to 2
            return slug

        slug = self.get_new_slug(model_instance)

        # exclude the current model instance from the queryset used in finding
        # the next valid slug
        if hasattr(model_instance, 'gen_slug_queryset'):
            queryset = model_instance.gen_slug_queryset()
        else:
            queryset = model_instance.__class__._default_manager.all()
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        kwargs = {self.attname: slug}
        while queryset.filter(**kwargs).count() > 0:
            slug = self.get_new_slug(model_instance, random.random())
            kwargs[self.attname] = slug

        return slug

    def pre_save(self, model_instance, add):
        value = self.create_slug(model_instance, add)
        setattr(model_instance, self.attname, value)
        return value

    def get_internal_type(self):
        return "SlugField"
