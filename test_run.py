import unittest
import riddler
from mock import mock_open, MagicMock, patch, call

m = mock_open()
with patch('__main__.open', m, create=True):
     with open('data/users.txt', 'w') as h:
         h.write('some stuff')

m.mock_calls
[call('foo', 'w'),
call().__enter__(),
call().write('some stuff'),
call().__exit__(None, None, None)]
m.assert_called_once_with('foo', 'w')
handle = m()
handle.write.assert_called_once_with('some stuff')    