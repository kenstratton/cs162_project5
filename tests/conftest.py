import pytest
import os
import sys

# Add the path of the directory one level above to the list of module searching paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import *

# Preparation of data for tests
@pytest.fixture(scope="module", params=[(Application(), VALUES[0])])
def setup(request):
    request.param[0].txt_box.insert(
        0, request.param[1])
    yield {"app":request.param[0], "target":request.param[1]}