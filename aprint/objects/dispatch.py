from typing import *

ParameterType = Union[Type, bool, int, str, None]
ParametersType = Tuple[ParameterType, ...]
ParametersFunc = Callable[[Any], ParametersType]

class APrintObj:
	def __init__(self):
		self.parameters_func: Dict[Type, ParametersFunc] = {}
		self.dispatch_dicts: Dict[Type, Union[Callable, Dict[ParametersType, Callable]]] = {}
		self.or_patch_dict: Dict[Type, Callable] = {}

	def parameters(self, type_obj: Type):
		def decorator(func):
			self.parameters_func[type_obj] = func
			return func
		return decorator

	def dispatch(self,
			*args,
		) -> Callable[[Callable], Callable]:
		# numpy sytle docstring
		"""
		"""
		assert len(args) >= 1, f"obj_dispatch([or_patch=False,] type_obj, *parameters) takes at least 1 argument ({len(args)} given)"
		if len(args) == 1:
			or_patch, type_obj, parameters = False, args[0], ()
		else:
			if isinstance(args[0], bool):
				or_patch, type_obj, parameters = args[0], args[1], ()
			else:
				or_patch, type_obj, parameters = False, args[0], args[1:]
		if not parameters:
			if type_obj in self.dispatch_dicts:
				assert isinstance(self.dispatch_dicts[type_obj], Dict), f"use @obj_dispatch({type_obj.__name__}, None) to set fallback function"
				print(f"Warning: @obj_dispatch({type_obj.__name__}) is overrided")
			if or_patch:
				self.or_patch_dict[type_obj] = None
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
		if or_patch:
			self.or_patch_dict[type_obj] = parameters
		def decorator(func):
			dispatch_dict[parameters] = func
			return func
		return decorator

	def or_patch(self, patch_type: Type, do_patch: bool = True):
		if not do_patch:
			for type_obj in self.or_patch_dict:
				type_obj.__or__ = self.or_patch_dict[type_obj]
			return
		for type_obj in self.or_patch_dict:
			ori_or = getattr(type_obj, "__or__")
			assert ori_or is not None, f"The original {type_obj.__name__}.__or__ is not defined"
			print(f"Warning: {type_obj.__name__}.__or__ is overrided")
			if self.or_patch_dict[type_obj] is None:
				self.or_patch_dict[type_obj] = ori_or
			def new_or(self, other):
				if isinstance(other, patch_type):
					raise NotImplementedError
				return ori_or(self, other)
			type_obj.__or__ = new_or

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
