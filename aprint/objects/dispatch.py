from typing import *

ParametersType = Tuple[Union[Type, bool, int, str, None], ...]
ParametersFunc = Callable[[Any], ParametersType]

class APrintObj:
	def __init__(self):
		self.parameters_func: Dict[Type, ParametersFunc] = {}
		self.dispatch_dicts: Dict[Type, Union[Callable, Dict[ParametersType, Callable]]] = {}

	def parameters(self, type_obj: Type):
		def decorator(func):
			self.parameters_func[type_obj] = func
			return func
		return decorator

	def dispatch(self, type_obj: Type, *parameters: ParametersType) -> Callable[[Callable], Callable]:
		if not parameters:
			if type_obj in self.dispatch_dicts:
				assert isinstance(self.dispatch_dicts[type_obj], Dict), f"use @obj_dispatch({type_obj.__name__}, None) to set fallback function"
				print(f"Warning: @obj_dispatch({type_obj.__name__}) is overrided")
			def decorator(func):
				self.dispatch_dicts[type_obj] = func
				return func
			return decorator
		if type_obj not in self.dispatch_dicts:
			self.dispatch_dicts[type_obj] = {}
		dispatch_dict = self.dispatch_dicts[type_obj]
		assert isinstance(dispatch_dict, Dict), f"conflict with @obj_dispatch({type_obj.__name__}) before"
		if len(parameters) == 1 and parameters[0] is None:
			parameters = None
		def decorator(func):
			dispatch_dict[parameters] = func
			return func
		return decorator

	def __call__(self, obj, *args, **kwargs):
		funcs = self.dispatch_dicts.get(type(obj), None)
		if funcs is None:
			return repr(obj)
		if callable(funcs):
			return funcs(obj, *args, **kwargs)
		parameters_func = self.parameters_func.get(type(obj), None)
		if parameters_func is None:
			return repr(obj)
		parameters = parameters_func(obj)
		func = funcs.get(parameters, None)
		if func is None:
			func = funcs.get(None, None) # fallback to Tuple[None] if not found
			if func is None:
				return repr(obj)
		return func(obj, *args, **kwargs)

aprintobj = APrintObj()
obj_parameters = aprintobj.parameters
obj_dispatch = aprintobj.dispatch
