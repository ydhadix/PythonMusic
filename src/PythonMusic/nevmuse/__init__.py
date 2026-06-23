"""
nevmuse package initialization.
"""

from .Surveyor import Surveyor
from .RunMetrics import RunMetrics
from .data import *
from .metrics import *
from .metrics.simple import *
from .utilities import *

# collect all symbols from sub-packages
from .data import __all__ as allData
from .metrics import __all__ as allMetrics
from .metrics.simple import __all__ as allSimple
from .utilities import __all__ as allUtilities

__all__ = ['Surveyor', 'RunMetrics'] + allData + allMetrics + allSimple + allUtilities
