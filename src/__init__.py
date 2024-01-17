"""
# quant-wheel
Wheels for quantitative research.

## See Also
### Github repository
* https://github.com/Chitaoji/quant-wheel/

### PyPI project
* https://pypi.org/project/quant-wheel/

## License
This project falls under the BSD 3-Clause License.

"""
#                          _                _               _
#   __ _ _   _  __ _ _ __ | |_    __      _| |__   ___  ___| |
#  / _` | | | |/ _` | '_ \| __|___\ \ /\ / / '_ \ / _ \/ _ \ |
# | (_| | |_| | (_| | | | | ||_____\ V  V /| | | |  __/  __/ |
#  \__, |\__,_|\__,_|_| |_|\__|     \_/\_/ |_| |_|\___|\___|_|
#     |_|
#                                                    @Chitaoji

import lazyr

lazyr.register("pandas")

# pylint: disable=wrong-import-position
from . import abcv, core, field, operator

__all__ = []
__all__.extend(abcv.__all__)
__all__.extend(core.__all__)
__all__.extend(field.__all__)
__all__.extend(operator.__all__)

from .__version__ import __version__
from .abcv import *
from .core import *
from .field import *
from .operator import *
