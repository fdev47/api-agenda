"""
Script para ejecutar todos los tests del servicio auth
"""
import os
import sys
import subprocess

def run_test(test_file):
    """Ejecutar un test específico"""
    print(f"\n🧪 Ejecutando: {test_file}")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join("tests", test_file)
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print(result.stdout)
        if result.stderr:
            print(f"❌ Errores: {result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando {test_file}: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🚀 Ejecutando todos los tests del servicio auth...")
    
    tests = [
        "debug_routes.py",
        "test_middleware_errors.py", 
        "test_complete_flow.py",
        "test_with_real_token.py"
    ]
    
    results = []
    
    for test in tests:
        success = run_test(test)
        results.append((test, success))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE TESTS")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{test:<25} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Resultado: {passed} pasaron, {failed} fallaron")
    
    if failed == 0:
        print("🎉 ¡Todos los tests pasaron!")
    else:
        print("⚠️  Algunos tests fallaron")

if __name__ == "__main__":
    main() 