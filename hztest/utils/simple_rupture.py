from typing import Optional
from dataclasses import dataclass, fields

from openquake.hazardlib.geo.point import Point


def add_slots(cls):

    # written by Eric V. Smith (https://github.com/ericvsmith/dataclasses/)

    # Need to create a new class, since we can't set __slots__
    #  after a class has been created.

    # Make sure __slots__ isn't already set.
    if '__slots__' in cls.__dict__:
        raise TypeError(f'{cls.__name__} already specifies __slots__')

    # Create a new dict for our new class.
    cls_dict = dict(cls.__dict__)
    field_names = tuple(f.name for f in fields(cls))
    cls_dict['__slots__'] = field_names
    for field_name in field_names:
        # Remove our attributes, if present. They'll still be
        #  available in _MARKER.
        cls_dict.pop(field_name, None)
    # Remove __dict__ itself.  NOTE: changed by RHS
    #cls_dict.pop('__dict__', None)
    # And finally create the class.
    qualname = getattr(cls, '__qualname__', None)
    cls = type(cls)(cls.__name__, cls.__bases__, cls_dict)
    if qualname is not None:
        cls.__qualname__ = qualname
    return cls


@add_slots
@dataclass
class SimpleRupture:
    strike: Optional[float] = None
    dip: Optional[float] = None
    rake: Optional[float] = None
    mag: Optional[float] = None
    hypocenter: Optional[Point] = None
    occurrence_rate: Optional[float] = None
    source: Optional[str] = None

    def __dict__(self):
        return {
            'strike': self.strike,
            'dip': self.dip,
            'rake': self.rake,
            'mag': self.mag,
            'hypocenter':
            [self.hypocenter.x, self.hypocenter.y, self.hypocenter.z],
            'occurrence_rate': self.occurrence_rate,
            'source': self.source
        }
