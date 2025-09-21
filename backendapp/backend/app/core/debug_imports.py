# debug_imports.py
# Run this to check what cache packages are available

print("Testing different import paths...")

# Test 1: fastapi_cache2 (original import)
try:
    from fastapi_cache2 import FastAPICache
    print("✅ fastapi_cache2.FastAPICache - WORKS")
except ImportError as e:
    print(f"❌ fastapi_cache2.FastAPICache - FAILED: {e}")

# Test 2: fastapi_cache 
try:
    from fastapi_cache import FastAPICache
    print("✅ fastapi_cache.FastAPICache - WORKS")
except ImportError as e:
    print(f"❌ fastapi_cache.FastAPICache - FAILED: {e}")

# Test 3: Check if fastapi_cache2 module exists at all
try:
    import fastapi_cache2
    print(f"✅ fastapi_cache2 module found at: {fastapi_cache2.__file__}")
    print(f"   Available attributes: {dir(fastapi_cache2)}")
except ImportError as e:
    print(f"❌ fastapi_cache2 module - FAILED: {e}")

# Test 4: Check if fastapi_cache module exists
try:
    import fastapi_cache
    print(f"✅ fastapi_cache module found at: {fastapi_cache.__file__}")
    print(f"   Available attributes: {dir(fastapi_cache)}")
except ImportError as e:
    print(f"❌ fastapi_cache module - FAILED: {e}")

# Test 5: Check specific backends
try:
    from fastapi_cache2.backends.redis import RedisBackend
    print("✅ fastapi_cache2.backends.redis.RedisBackend - WORKS")
except ImportError as e:
    print(f"❌ fastapi_cache2.backends.redis.RedisBackend - FAILED: {e}")

try:
    from fastapi_cache.backends.redis import RedisBackend
    print("✅ fastapi_cache.backends.redis.RedisBackend - WORKS")
except ImportError as e:
    print(f"❌ fastapi_cache.backends.redis.RedisBackend - FAILED: {e}")