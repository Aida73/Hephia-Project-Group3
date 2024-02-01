import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import stub
from train import train, launch
from inference import Inference
