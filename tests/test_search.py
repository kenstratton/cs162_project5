import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from search import *

# Whether the processing reaches the search through other methods
def test_process(mocker, setup):
    is_int = mocker.patch("search.Application.is_int")
    change_num_state = mocker.patch("search.Canvas.change_num_state")
    search = mocker.patch("search.BinarySearch.search")

    setup["app"].process()

    is_int.assert_called_once_with(str(setup["target"]))
    change_num_state.assert_called_once_with()
    search.assert_called_once_with(setup["target"], 0, len(VALUES)-1)

# Whether the search method expectedly outputs after executed
def test_search(mocker, setup):
    assert setup["app"].bi_search.records == []
    assert setup["app"].bi_search.search(
        setup["target"], 0, len(VALUES)-1) == True
    assert setup["app"].bi_search.search(
        0.5, 0, len(VALUES)-1) == False
    assert setup["app"].bi_search.records

# Whether the animation is executed with an expected argument
def test_animation(mocker, setup):
    animation = mocker.patch("search.Canvas.animation")
    setup["app"].process()

    animation.assert_called_once_with(True, str(setup["target"]))