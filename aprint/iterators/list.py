from .dispatch import iter_dispatch

@iter_dispatch(list)
def aprint_list(obj):
	leading_str = f"[ # list with len={len(obj)}"
	trailing_str = "]"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str
