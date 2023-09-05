from .dispatch import iter_dispatch

@iter_dispatch(dict)
def aprint_dict(obj):
	leading_str = f"{{ # dict with len={len(obj)}"
	trailing_str = "}"
	def item_func(item):
		return obj[item], f"{repr(item)}: ", ","
	return item_func, leading_str, trailing_str
