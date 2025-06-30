# app/scripts/check_profile_service.py
"""
Script to check what methods are available in ProfileService
"""

import sys
import os

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.services.profile_service import ProfileService
    
    print("🔍 ProfileService Methods Available:")
    print("=" * 40)
    
    methods = [method for method in dir(ProfileService) if not method.startswith('_')]
    
    for method in methods:
        print(f"✅ {method}")
    
    print(f"\n📊 Total methods: {len(methods)}")
    
    # Check specifically for validate_profile_completeness
    if hasattr(ProfileService, 'validate_profile_completeness'):
        print("\n✅ validate_profile_completeness method EXISTS")
    else:
        print("\n❌ validate_profile_completeness method MISSING")
        print("\nThis is causing your error!")
    
    # Check the method exists and is callable
    try:
        method = getattr(ProfileService, 'validate_profile_completeness', None)
        if method:
            print(f"   Method type: {type(method)}")
            print(f"   Is callable: {callable(method)}")
        else:
            print("   Method is None")
    except Exception as e:
        print(f"   Error accessing method: {e}")

except ImportError as e:
    print(f"❌ Could not import ProfileService: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()