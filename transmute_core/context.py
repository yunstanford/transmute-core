from .object_serializers import get_default_object_serializer_set
from .contenttype_serializers import get_default_serializer_set
from .response_shape import ResponseShapeSimple


class TransmuteContext(object):
    """
    TransmuteContext contains all of the configuration points for a
    framework based off of transmute.

    It is useful for customizing default behaviour in Transmute, such
    as serialization of additional content types, or using different
    serializers for objects to and from basic data times.
    """

    def __init__(
        self, serializers=None, contenttype_serializers=None, response_shape=None
    ):
        self.serializers = serializers or get_default_object_serializer_set()
        self.contenttype_serializers = (
            contenttype_serializers or get_default_serializer_set()
        )
        self.response_shape = ResponseShapeSimple


# a global context is provided, if a singleton is sufficient
# or deviations from the defaults are unnescessary
default_context = TransmuteContext()
