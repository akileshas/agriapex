import os
import sys
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from utils.data import (
    get_states,
)
