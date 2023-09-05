from .dispatch import iter_dispatch

@iter_dispatch(tuple)
def aprint_tuple(obj):
	leading_str = f"( # tuple with len={len(obj)}"
	trailing_str = ")"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str
