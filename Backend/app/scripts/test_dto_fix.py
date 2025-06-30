# app/scripts/test_dto_fix.py
"""
Test script to verify that the DTO fix is working correctly
"""

import sys
import os

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_db
from app.services.dal.document_dal import DocumentTypeDal
from app.services.profile_service import ProfileService

def test_document_type_dto():
    """Test that DocumentTypeDTO is working correctly"""
    print("🧪 Testing DocumentTypeDTO")
    print("=" * 40)
    
    try:
        db = next(get_db())
        
        # Test getting all document types
        doc_types = DocumentTypeDal.get_all_document_types(db)
        print(f"✅ Retrieved {len(doc_types)} document types as DTOs")
        
        if doc_types:
            # Test first few DTOs
            for i, dt in enumerate(doc_types[:3]):
                print(f"\n📄 DTO {i+1}: {dt.name_english}")
                print(f"   Type: {type(dt)}")
                print(f"   ID: {dt.id}")
                print(f"   Category: '{dt.category}' (type: {type(dt.category)})")
                print(f"   Instructions: '{dt.instructions}' (type: {type(dt.instructions)})")
                print(f"   Is Mandatory: {dt.is_mandatory} (type: {type(dt.is_mandatory)})")
                
                # Test to_dict method
                dto_dict = dt.to_dict()
                print(f"   DTO Dict Keys: {list(dto_dict.keys())}")
                
                # Check for null values
                null_fields = [k for k, v in dto_dict.items() if v is None]
                if null_fields:
                    print(f"   ⚠️  Null fields in DTO: {null_fields}")
                else:
                    print(f"   ✅ No null fields in DTO")
        
        return True
        
    except Exception as e:
        print(f"❌ DocumentTypeDTO test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'db' in locals():
            db.close()

def test_profile_service():
    """Test that ProfileService methods work with DTOs"""
    print("\n🧪 Testing ProfileService with DTOs")
    print("=" * 40)
    
    try:
        db = next(get_db())
        
        # Test get_document_types
        print("1️⃣ Testing get_document_types...")
        doc_types = ProfileService.get_document_types(db)
        print(f"   ✅ Retrieved {len(doc_types)} document types")
        
        if doc_types:
            sample = doc_types[0]
            print(f"   📄 Sample response structure:")
            for key, value in sample.items():
                if value is None:
                    print(f"      {key}: NULL ❌")
                else:
                    print(f"      {key}: {type(value).__name__} ✅")
        
        # Test category filtering
        print("\n2️⃣ Testing category filtering...")
        identity_docs = ProfileService.get_document_types(db, category="identity_proof")
        print(f"   ✅ Found {len(identity_docs)} identity proof documents")
        
        # Test get_document_categories
        print("\n3️⃣ Testing get_document_categories...")
        categories = ProfileService.get_document_categories()
        print(f"   ✅ Retrieved {len(categories)} categories")
        
        return True
        
    except Exception as e:
        print(f"❌ ProfileService test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'db' in locals():
            db.close()

def test_validation_method():
    """Test the updated validation method"""
    print("\n🧪 Testing ProfileService.validate_profile_completeness")
    print("=" * 55)
    
    try:
        db = next(get_db())
        
        # Test with user ID 8 (from your example)
        validation_result = ProfileService.validate_profile_completeness(db, user_id=8)
        
        print(f"✅ Validation completed successfully")
        print(f"📊 Completion: {validation_result['completionPercentage']}%")
        print(f"📋 Missing documents: {len(validation_result['missingMandatoryDocuments'])}")
        
        # Check if missing documents have proper category/instructions
        if validation_result['missingMandatoryDocuments']:
            print(f"\n📄 Sample missing document:")
            sample_missing = validation_result['missingMandatoryDocuments'][0]
            for key, value in sample_missing.items():
                if value is None:
                    print(f"   {key}: NULL ❌")
                else:
                    print(f"   {key}: '{value}' ✅")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'db' in locals():
            db.close()

def main():
    """Run all tests"""
    print("🚀 DTO Fix Test Suite")
    print("=" * 30)
    
    tests = [
        ("DocumentTypeDTO", test_document_type_dto),
        ("ProfileService", test_profile_service),
        ("Validation Method", test_validation_method)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! DTO fix is working correctly.")
        print("\n🔗 Your API should now return proper categories and instructions!")
        print("\nTest your endpoints:")
        print("   GET /v1/profile/me")
        print("   GET /v1/profile/document-types")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)