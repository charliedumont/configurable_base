from contextlib2 import contextmanager
from google.appengine.api import datastore_types
from mock import patch
from freezegun import freeze_time as _freeze_time
from freezegun.api import FakeDatetime

@contextmanager
def freeze_time(*args, **kwargs):
    with patch('google.appengine.ext.db.DateTimeProperty.data_type',
                new=FakeDatetime):
        datastore_types._VALIDATE_PROPERTY_VALUES[FakeDatetime] = \
            datastore_types.ValidatePropertyNothing
        datastore_types._PACK_PROPERTY_VALUES[FakeDatetime] = \
            datastore_types.PackDatetime
        datastore_types._PROPERTY_MEANINGS[FakeDatetime] = \
            datastore_types.entity_pb.Property.GD_WHEN

        with _freeze_time(*args, **kwargs):
            yield

