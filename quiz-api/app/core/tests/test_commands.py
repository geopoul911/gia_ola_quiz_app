from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    # test waiting for db until db is available
    def test_wait_for_db_ready(self):
        # mock getitem which will always return True
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # test wait for db
    @patch('time.sleep', return_value=True)  # replace time.sleep with return True. keep our tests fast
    def test_wait_for_db(self, ts):
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
