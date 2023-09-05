from .dispatch import iter_dispatch

@iter_dispatch(set)
def aprint_set(obj) -> set:
	leading_str = f"{{ # set with len={len(obj)}"
	trailing_str = "}"
	def item_func(item):
		return item, "", ","
	return item_func, leading_str, trailing_str
