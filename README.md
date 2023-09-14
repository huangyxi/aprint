# aprint

A Python print package for those who don't care the actual elements of array-like data (e.g. `numpy.array`, `torch.tensor`) within a complex data structure.


## Background

By default, `print` will display the actual elements in array-like data, such as `numpy.array` or `torch.tensor`, which is not very friendly for those who don't care about the actual elements.
Inspired by the leading scientific computing language [Julia](https://julialang.org/), this package will print the **type and shape** of the data structure, as well as the **type and shape** of the elements within the data structure.


## Installation

```
pip install aprint
```

For the latest version, you can install from github:
```
pip install git+https://github.com/huangyuxi/aprint.git
```

## Usage

```python
>>> import numpy as np
>>> import torch
>>> from aprint import aprint

>>> aprint(np.array([1, 2, 3]))
int64[3] numpy.ndarray

>>> aprint({'a': torch.zeros(16, 32).cuda(), 2: [np.array([1, 2]), (torch.zeros(2).to_sparse(), torch.zeros(2,3).to_sparse_csr(), torch.zeros(2,3,4).to_sparse_csc()), {'5', 6, 7.}]}, indent_str='| ')
{ # dict with len=2
| 'a': float32[16×32] torch.Tensor at 'cuda:0' with grad=False,
| 2: [ # list with len=3
| | int64[2] numpy.ndarray,
| | ( # tuple with len=3
| | | float32[2] torch.Tensor at 'cpu' with layout='COO', grad=False,
| | | float32[2×3] torch.Tensor at 'cpu' with layout='CSR', grad=False,
| | | float32[2×3×4] torch.Tensor at 'cpu' with layout='CSC', grad=False,
| | ),
| | { # set with len=3
| | | '5',
| | | 6,
| | | 7.0,
| | },
| ],
}

>>> aprint([1, [2, [3, [4, [5]]]]], max_depth=3, indent_str="⋮ ") # default max_depth=5
[ # list with len=2
⋮ 1,
⋮ [ # list with len=2
⋮ ⋮ 2,
⋮ ⋮ [ # list with len=2
⋮ ⋮ ⋮ 3,
⋮ ⋮ ⋮ [ # list with len=2 ... ],
⋮ ⋮ ],
⋮ ],
]

>>> torch.tensor([1, 2]) | aprint # pipeline print (only for torch.Tensor and built-in iterators)
int64[2] torch.Tensor at 'cpu' with grad=False
```

## Roadmap

- [x] pipeline support for `torch.Tensor`
- [ ] continuous integration
- [ ] support class inheritance
  - [x] support iterators' classes
  - [ ] support objects' classes
- [ ] support more types
  - [ ] `torch.nn.parameter.Parameter`
- [ ] colorful output
- [ ] glance of the data


## License

MIT License
