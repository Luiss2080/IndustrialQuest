# -*- coding: utf-8 -*-
"""
Sistema de almacenamiento compatible con Pygame4Web.
Abstracción que usa localStorage en navegador y JSON en escritorio.
"""
import json
import os
import sys

class AlmacenamientoPersistente:
    """
    Clase que abstrae el almacenamiento local.
    En navegador usa localStorage vía JavaScript.
    En escritorio usa archivos JSON.
    """
    
    def __init__(self, nombre_archivo="production_logs.json"):
        self.nombre_archivo = nombre_archivo
        self.es_navegador = self._detectar_navegador()
        self.datos_cache = {}
        self.cargar()
    
    def _detectar_navegador(self):
        """Detecta si estamos en navegador o escritorio"""
        return hasattr(sys, 'emscripten') or 'emscripten' in sys.platform
    
    def _usar_javascript(self, codigo_js):
        """Ejecuta código JavaScript si estamos en navegador"""
        try:
            import asyncio
            import js
            return eval(codigo_js)
        except:
            return None
    
    def cargar(self):
        """Carga los datos desde localStorage o JSON"""
        if self.es_navegador:
            try:
                import js
                datos_json = js.localStorage.getItem("industrial_quest_data")
                if datos_json:
                    self.datos_cache = json.loads(datos_json)
                else:
                    self.datos_cache = self._estructura_defecto()
            except:
                self.datos_cache = self._estructura_defecto()
        else:
            # Modo escritorio: cargar desde JSON
            if os.path.exists(self.nombre_archivo):
                try:
                    with open(self.nombre_archivo, "r", encoding="utf-8") as f:
                        self.datos_cache = json.load(f)
                except:
                    self.datos_cache = self._estructura_defecto()
            else:
                self.datos_cache = self._estructura_defecto()
    
    def guardar(self):
        """Guarda los datos en localStorage o JSON"""
        if self.es_navegador:
            try:
                import js
                js.localStorage.setItem("industrial_quest_data", json.dumps(self.datos_cache))
            except:
                print("Advertencia: No se pudieron guardar datos en localStorage")
        else:
            # Modo escritorio
            try:
                with open(self.nombre_archivo, "w", encoding="utf-8") as f:
                    json.dump(self.datos_cache, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Advertencia: Error al guardar datos: {e}")
    
    def _estructura_defecto(self):
        """Retorna la estructura de datos por defecto"""
        return {
            "logs": [],
            "volumen_musica": 0.5,
            "volumen_sfx": 0.7,
            "velocidad_ajustada": 1.0,
            "niveles_completados": []
        }
    
    def obtener(self, clave, defecto=None):
        """Obtiene un valor del almacenamiento"""
        return self.datos_cache.get(clave, defecto)
    
    def establecer(self, clave, valor):
        """Establece un valor en el almacenamiento"""
        self.datos_cache[clave] = valor
        self.guardar()
    
    def agregar_log(self, log):
        """Añade un log a la lista de historico"""
        logs = self.datos_cache.get("logs", [])
        logs.append(log)
        self.datos_cache["logs"] = logs
        self.guardar()
    
    def obtener_todos_los_datos(self):
        """Retorna una copia de todos los datos"""
        return self.datos_cache.copy()
