from django.test import TestCase
from ..models import LogRecordsModel
import uuid


class LogRecordsModelTestCase(TestCase):
    """LogRecordsModelTestCase holds and perform the initial test cases for the model of LogRecordsModel.
       It initialize and create some test values and run various tests depends on the value. If you want
       to run your own tests then you may extend this class and run your testcase here"""
    uuid_default_id = uuid.uuid4()

    def setUp(self):
        """Setting up some fake datas depends on various scenarios"""
        LogRecordsModel.objects.create()
        LogRecordsModel.objects.create(actor_id='25', log_detail='Test Log', targeted_instance_id='10',
                                       event_path='/views/detail/1/')

        """Lets create an object where actor_id is uuid.uuid4() types"""
        LogRecordsModel.objects.create(actor_id=self.uuid_default_id, log_detail='A UUID test log',
                                       targeted_instance_id=self.uuid_default_id,
                                       event_path='/views/%s/' % str(self.uuid_default_id))

    def test_log_records_default_data(self):
        """Testing if database default data are working properly"""
        test_object = LogRecordsModel.objects.get(id=1)
        self.assertEqual(test_object.actor_id, '0')
        self.assertEqual(test_object.log_detail, 'n/a')
        self.assertEqual(test_object.targeted_instance_id, '0')
        self.assertEqual(test_object.event_path, 'n/a')

    def test_log_records_inserted_data(self):
        """Testing if database inserted data are working properly"""
        test_object = LogRecordsModel.objects.get(id=2)
        self.assertEqual(test_object.actor_id, '25')
        self.assertEqual(test_object.log_detail, 'Test Log')
        self.assertEqual(test_object.targeted_instance_id, '10')
        self.assertEqual(test_object.event_path, '/views/detail/1/')

    def test_log_records_uuid_inserted_data(self):
        """Testing if database using uuid.uuid4() as the ID number"""
        test_object = LogRecordsModel.objects.get(id=3)
        self.assertEqual(test_object.actor_id, str(self.uuid_default_id))
        self.assertEqual(test_object.log_detail, 'A UUID test log')
        self.assertEqual(test_object.targeted_instance_id, str(self.uuid_default_id))
        self.assertEqual(test_object.event_path, '/views/%s/' % str(self.uuid_default_id))
