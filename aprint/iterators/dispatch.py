from typing import *

IterAPrintFunc = Callable[[Any], Tuple[Callable[[Any], Tuple[Any, str, str]], str, str]]

class APrintIter:
	def __init__(self):
		self.max_len = 1024 # prevent possible infinite loops
		self.dispatch_dicts: Dict[Type, IterAPrintFunc] = {}

	def dispatch(self, type_objs: Union[Type, List[Type]]):
		if isinstance(type_objs, Type):
			type_objs = [type_objs]
		def decorator(func):
			for type_obj in type_objs:
				self.dispatch_dicts[type_obj] = func
			return func
		return decorator

	def iterable(self, obj: Any):
		return type(obj) in self.dispatch_dicts

	def __call__(self, obj, *args, **kwargs):
		func = self.dispatch_dicts.get(type(obj), None)
		if func is not None:
			return func(obj, *args, **kwargs)
		parents = type(obj).__mro__
		for parent in parents[1:-1]:
			func = self.dispatch_dicts.get(parent, None)
			if func is None:
				continue
			if len(self.dispatch_dicts) < self.max_len:
				self.dispatch_dicts[type(obj)] = func
			return func(obj, *args, **kwargs)
		return lambda item: (item, "", ""), "", ""

aprintiter = APrintIter()
iter_dispatch = aprintiter.dispatch
