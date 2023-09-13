from typing import Any

from .iterators import aprintiter
from .objects import aprintobj


class APrint:
	def __init__(
		self,
		obj: Any,
		depth: int = 0, # current depth of recursion
		max_depth: int = 5, # max depth of recursion
		indent_str: str = "  ", # indent string
		start_str: str = "", # string to print before the object
	):
		self.obj = obj
		self.depth = depth
		self.max_depth = max_depth
		self.indent_str = indent_str
		self.start_str = start_str

	def __str__(self):
		repr_str = ""
		repr_str += self.indent_str * self.depth
		repr_str += self.start_str
		if not aprintiter.iterable(self.obj):
			repr_str += aprintobj(self.obj)
			return repr_str
		item_func, leading_str, trailing_str = aprintiter(self.obj)
		repr_str += leading_str
		if self.depth >= self.max_depth:
			repr_str += " ... "
			repr_str += trailing_str
			return repr_str
		repr_str += "\n"
		for item in self.obj:
			item, start_str, end_str = item_func(item)
			repr_str += str(APrint(
				item,
				depth=self.depth+1,
				max_depth=self.max_depth,
				indent_str=self.indent_str,
				start_str=start_str
			))
			repr_str += end_str
			repr_str += "\n"
		repr_str += self.indent_str * self.depth
		repr_str += trailing_str
		return repr_str


class APrintFunc:
	@staticmethod
	def __call__(
		*objects: Any,
		max_depth: int = 5,
		indent_str: str = "| ",
		**kwargs
	):
		aprint_func = lambda obj: APrint(
			obj,
			max_depth=max_depth,
			indent_str=indent_str
		)
		print(*map(aprint_func, objects), **kwargs)

	def __ror__(self, value: Any):
		self(value)

	@classmethod
	def or_patch(cls, do_patch: bool = True):
		aprintobj.or_patch(cls, do_patch=do_patch)

aprint = APrintFunc()
