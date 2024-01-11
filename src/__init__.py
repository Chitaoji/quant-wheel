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
