#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación pre-deploy para IndustrialQuest.
Verifica que todas las dependencias y archivos necesarios existen antes de deployar.
"""

import os
import sys
import json

def verificar_archivo(ruta, descripcion):
    """Verifica que un archivo existe"""
    existe = os.path.exists(ruta)
    estado = "✓" if existe else "✗"
    print(f"  {estado} {descripcion}")
    return existe

def verificar_directorio(ruta, descripcion):
    """Verifica que un directorio existe"""
    existe = os.path.isdir(ruta)
    estado = "✓" if existe else "✗"
    print(f"  {estado} {descripcion}")
    return existe

def main():
    print("=" * 50)
    print("  IndustrialQuest Pre-Deploy Verification")
    print("=" * 50)
    print()
    
    errores = []
    
    # Verificar archivos principales
    print("Verificando archivos principales...")
    if not verificar_archivo("main.py", "main.py (entrada)"):
        errores.append("main.py no encontrado")
    if not verificar_archivo("pyproject.toml", "pyproject.toml"):
        errores.append("pyproject.toml no encontrado")
    if not verificar_archivo("index.html", "index.html"):
        errores.append("index.html no encontrado")
    if not verificar_archivo("netlify.toml", "netlify.toml"):
        errores.append("netlify.toml no encontrado")
    print()
    
    # Verificar directorios
    print("Verificando directorios...")
    if not verificar_directorio("src", "Directorio src/"):
        errores.append("Directorio src/ no encontrado")
    if not verificar_directorio("recursos", "Directorio recursos/"):
        errores.append("Directorio recursos/ no encontrado")
    if not verificar_directorio("recursos/imagenes", "Directorio recursos/imagenes/"):
        errores.append("Directorio recursos/imagenes/ no encontrado")
    if not verificar_directorio("recursos/sonidos", "Directorio recursos/sonidos/"):
        errores.append("Directorio recursos/sonidos/ no encontrado")
    if not verificar_directorio("fonts", "Directorio fonts/"):
        errores.append("Directorio fonts/ no encontrado")
    print()
    
    # Verificar módulos Python principales
    print("Verificando módulos Python...")
    modulos = ["src/motor.py", "src/constantes.py", "src/administrador_recursos.py", "src/almacenamiento.py"]
    for modulo in modulos:
        if not verificar_archivo(modulo, f"Módulo {modulo}"):
            errores.append(f"Módulo {modulo} no encontrado")
    print()
    
    # Verificar archivo de requisitos
    print("Verificando dependencias...")
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            contenido = f.read().strip()
            if "pygame" in contenido.lower():
                print("  ✓ pygame-ce en requirements.txt")
            else:
                print("  ✗ pygame-ce no está en requirements.txt")
                errores.append("pygame-ce falta en requirements.txt")
    else:
        print("  ✗ requirements.txt no encontrado")
        errores.append("requirements.txt no encontrado")
    print()
    
    # Verificar recursos multimedia
    print("Verificando recursos multimedia...")
    imagenes = os.listdir("recursos/imagenes") if os.path.isdir("recursos/imagenes") else []
    sonidos = os.listdir("recursos/sonidos") if os.path.isdir("recursos/sonidos") else []
    
    print(f"  ✓ {len(imagenes)} imágenes encontradas")
    print(f"  ✓ {len(sonidos)} sonidos encontrados")
    
    if len(imagenes) == 0:
        print("  ⚠ ADVERTENCIA: No hay imágenes en recursos/imagenes/")
    if len(sonidos) == 0:
        print("  ⚠ ADVERTENCIA: No hay sonidos en recursos/sonidos/")
    print()
    
    # Resultado final
    print("=" * 50)
    if errores:
        print("❌ ERRORES ENCONTRADOS:")
        for error in errores:
            print(f"   - {error}")
        print()
        print("Soluciona los errores antes de deployar.")
        return 1
    else:
        print("✅ ¡Todo está listo para deployar!")
        print()
        print("Pasos siguientes:")
        print("  1. Haz build localmente: python build.bat (Windows)")
        print("  2. Prueba: python -m http.server 8000 --directory build/web")
        print("  3. Commit y push a GitHub")
        print("  4. Netlify deployará automáticamente")
        print()
        return 0

if __name__ == "__main__":
    sys.exit(main())
