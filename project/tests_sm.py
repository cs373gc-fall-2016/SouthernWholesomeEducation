# pylint: disable=W0401,W0614,R0904,E1101
#!/usr/bin/env python3
# 24 * 3 tests
'''
Unit tests for models.py
'''

# -------
# imports
# -------

from unittest import main, TestCase
from models import *

# ----
# test
# ----


class Tests(TestCase):
    '''
        Unit tests for models.py
        '''

    # ----------------
    # university query
    # ----------------

    def test_university_1(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='University of East-West Medicine').first()
        self.assertEqual(uni.num_undergrads, 1066)



# ----
# main
# ----

if __name__ == "__main__":
    main()

