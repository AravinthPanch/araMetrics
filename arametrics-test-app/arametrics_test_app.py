#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : Test App

import sys
import datetime
from config.config import *
from secrets.keys import *

if __name__ == '__main__':
    print('========== arametrics-test-app ==========')
    print(datetime.datetime.now())
    print(TEST_API_ENDPOINT)
    print(TEST_API_KEY)
