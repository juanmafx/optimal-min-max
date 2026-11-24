from hypothesis import settings

settings.register_profile("reproducible", database=None, derandomize=True, max_examples=300)
settings.load_profile("reproducible")
