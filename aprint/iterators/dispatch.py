from typing import *

IterAPrintFunc = Callable[[Any], Tuple[Callable[[Any], Tuple[Any, str, str]], str, str]]

class APrintIter:
	def __init__(self):
		self.dispatch_dicts: Dict[Type, IterAPrintFunc] = {}

	def dispatch(self, type_obj: Type):
		def decorator(func):
			self.dispatch_dicts[type_obj] = func
			return func
		return decorator

	def iterable(self, obj: Any):
		return type(obj) in self.dispatch_dicts

	def __call__(self, obj, *args, **kwargs):
		func = self.dispatch_dicts.get(type(obj), None)
		if func is None:
			return lambda item: (item, "", ""), "", ""
		return func(obj, *args, **kwargs)

aprintiter = APrintIter()
iter_dispatch = aprintiter.dispatch
