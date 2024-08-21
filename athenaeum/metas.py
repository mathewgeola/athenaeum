import six


class BasesAttrsMergeMeta(type):
    def __new__(cls, name, bases, attrs):
        temp_attrs = dict()
        for base in bases:
            base_attrs = base.__dict__
            for base_attr_name, base_attr_value in base_attrs.items():
                if base_attr_name not in temp_attrs:
                    if not base_attr_name.startswith('__') and not base_attr_name.endswith('__'):
                        temp_attrs[base_attr_name] = base_attr_value
        temp_attrs.update(attrs)
        attrs = temp_attrs
        return super().__new__(cls, name, bases, attrs)


def gen_base_class_with_metaclass(*base_classes,
                                  extra_base_class_metas: tuple = tuple()):
    extra_base_class_metas = extra_base_class_metas + tuple(type(base_class) for base_class in base_classes)
    return six.with_metaclass(type('BaseClassMeta', extra_base_class_metas, {}), *tuple(base_classes))
