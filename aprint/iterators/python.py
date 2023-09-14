# Python built-in iterators
import collections

from .dispatch import iter_dispatch

def get_class_name(obj):
	class_name = type(obj).__name__
	module_name = type(obj).__module__
	if module_name == "builtins":
		return class_name
	else:
		return f"{module_name}.{class_name}"

@iter_dispatch([dict, collections.OrderedDict, collections.defaultdict])
def aprint_dict(obj):
	leading_str = f"{{ # {get_class_name(obj)} with len={len(obj)}"
	trailing_str = "}"
	def item_func(item):
		return obj[item], f"{repr(item)}: ", ","
	return item_func, leading_str, trailing_str


@iter_dispatch(list)
def aprint_list(obj):
	leading_str = f"[ # {get_class_name(obj)} with len={len(obj)}"
	trailing_str = "]"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str


@iter_dispatch(set)
def aprint_set(obj) -> set:
	leading_str = f"{{ # {get_class_name(obj)} with len={len(obj)}"
	trailing_str = "}"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str


@iter_dispatch(tuple)
def aprint_tuple(obj):
	leading_str = f"( # {get_class_name(obj)} with len={len(obj)}"
	trailing_str = ")"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str
