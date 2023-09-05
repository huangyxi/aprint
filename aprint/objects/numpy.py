from typing import Tuple
import numpy as np

from .dispatch import obj_dispatch

def shape_str(shape: Tuple[int, ...]):
	return f"{'×'.join(map(str, shape))}"

def dtype_str(dtype: np.dtype):
	return repr(dtype).removeprefix("dtype('").removesuffix("')")

def dtype_shape_str(obj: np.ndarray):
	return f"{dtype_str(obj.dtype)}[{shape_str(obj.shape)}]"

@obj_dispatch(np.ndarray)
def aprint_numpy_ndarray(obj):
	return f"{dtype_shape_str(obj)} numpy.ndarray"
