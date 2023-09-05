import torch

from .dispatch import obj_parameters, obj_dispatch

@obj_parameters(torch.Tensor)
def aprint_torch_tensor_parameters(obj):
	is_sparse = obj.layout != torch.strided
	return (is_sparse, )


def dtype_str(dtype: torch.dtype):
	return repr(dtype).removeprefix("torch.")

def shape_str(size: torch.Size):
	return f"{'×'.join(map(str, size))}"

def dtype_size_str(obj: torch.Tensor):
	return f"{dtype_str(obj.dtype)}[{shape_str(obj.shape)}]"


@obj_dispatch(torch.Tensor, None) # fallback function
def aprint_torch_tensor(obj: torch.Tensor):
	return f"{dtype_size_str(obj)} torch.Tensor at '{obj.device}' with grad={obj.requires_grad}"

@obj_dispatch(torch.Tensor, False)
def aprint_torch_tensor_dense(obj: torch.Tensor):
	return f"{dtype_size_str(obj)} torch.Tensor at '{obj.device}' with grad={obj.requires_grad}"

@obj_dispatch(torch.Tensor, True)
def aprint_torch_tensor_sparse(obj: torch.Tensor):
	layout = obj.layout
	layout_str = repr(layout).removeprefix("torch.sparse_").upper()
	return f"{dtype_size_str(obj)} torch.Tensor at '{obj.device}' with layout='{layout_str}', grad={obj.requires_grad}"
