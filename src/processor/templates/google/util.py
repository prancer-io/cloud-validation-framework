from jinja2 import Undefined
from jinja2._compat import implements_to_string, string_types
from jinja2.utils import missing, object_type_repr
from processor.logging.log_handler import getlogger

logger = getlogger()

class ResourceContext(object):

    def __init__(self, properties={}, **kwargs):
        self.properties = properties
    
    def __getattribute__(self, name):
        __dict__ = super(ResourceContext, self).__getattribute__('__dict__')
        value = {}
        if name in __dict__:
            value = object.__getattribute__(self, name)
        return value


@implements_to_string
class SilentUndefined(Undefined):
    '''
    handle undefined variables
    '''
    def _fail_with_undefined_error(self, *args, **kwargs):
        if self._undefined_hint is None:
            if self._undefined_obj is missing:
                hint = '%r is undefined' % self._undefined_name
            elif not isinstance(self._undefined_name, string_types):
                hint = '%s has no element %r' % (
                    self._undefined_obj,
                    self._undefined_name
                )
            else:
                hint = '%r has no attribute %r' % (
                    self._undefined_obj,
                    self._undefined_name
                )
        else:
            hint = self._undefined_hint
        logger.error(hint)
        return ''

    __slots__ = ()
    __iter__ = __str__ = __len__ = __nonzero__ = __eq__ = \
        __ne__ = __bool__ = __hash__ = \
        _fail_with_undefined_error
    
    def __getattr__(self, name):
        if name[:2] == '__':
            raise AttributeError(name)
        return self._fail_with_undefined_error()

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
        __float__ = __complex__ = __pow__ = __rpow__ = __sub__ = \
        __rsub__ = _fail_with_undefined_error

    def __eq__(self, other):
        return type(self) is type(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return id(type(self))

    def __str__(self):
        return u''

    def __len__(self):
        return 0

    def __iter__(self):
        if 0:
            yield None

    def __nonzero__(self):
        return False
    __bool__ = __nonzero__

    def __repr__(self):
        return 'Undefined'