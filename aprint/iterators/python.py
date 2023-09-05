# Python built-in iterators
from .dispatch import iter_dispatch


@iter_dispatch(dict)
def aprint_dict(obj):
	leading_str = f"{{ # dict with len={len(obj)}"
	trailing_str = "}"
	def item_func(item):
		return obj[item], f"{repr(item)}: ", ","
	return item_func, leading_str, trailing_str


@iter_dispatch(list)
def aprint_list(obj):
	leading_str = f"[ # list with len={len(obj)}"
	trailing_str = "]"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str


@iter_dispatch(set)
def aprint_set(obj) -> set:
	leading_str = f"{{ # set with len={len(obj)}"
	trailing_str = "}"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str


@iter_dispatch(tuple)
def aprint_tuple(obj):
	leading_str = f"( # tuple with len={len(obj)}"
	trailing_str = ")"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str
