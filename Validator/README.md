# EJERCICIO — Validador Modular de Formularios

## DESCRIPCIÓN

Debes implementar un sistema de validación modular para formularios de registro. Cada regla de validación es un objeto independiente, y el Validador las compone juntas.

Este patrón es muy común en aplicaciones web seguras para prevenir inyecciones y datos maliciosos.

## PALABRAS PROHIBIDAS

Las siguientes palabras no pueden aparecer en ningún campo (comparación sin distinción de mayúsculas/minúsculas):
```python
    ["admin", "root", "hack", "drop", "select", "delete"]
```

## CLASES QUE DEBES IMPLEMENTAR

1. Regla (clase abstracta base)
   - Método abstracto: validar(valor: str) -> bool
       * Retorna True si el valor cumple la regla.
   - Método abstracto: mensaje_error() -> str
       * Retorna un mensaje descriptivo del error.

2. ReglaNoPalabrasProhibidas(Regla)
   - Atributo de clase: PALABRAS_PROHIBIDAS (lista de palabras)
   - validar(valor):
       * Retorna True si el valor NO contiene ninguna
         palabra prohibida (comparación case-insensitive).
       * Retorna False si contiene al menos una.
   - mensaje_error():
       * Retorna: "El valor contiene palabras prohibidas"

3. ReglaLongitud(Regla)
   - Constructor: __init__(self, minimo: int, maximo: int)
       * Si minimo < 0, lanza ValueError("El mínimo no puede ser negativo")
       * Si maximo < minimo, lanza ValueError("El máximo no puede ser menor al mínimo")
   - validar(valor):
       * Retorna True si len(valor) >= minimo Y len(valor) <= maximo.
   - mensaje_error():
       * Retorna: "La longitud debe estar entre <minimo> y <maximo>"
       * Ejemplo: "La longitud debe estar entre 3 y 50"

4. ReglaFormatoEmail(Regla)
   - validar(valor):
       * Retorna True si el valor tiene formato de email básico.
       * Un email básico válido cumple TODOS estos criterios:
           - Contiene exactamente UN solo "@"
           - La parte antes del "@" (usuario) no está vacía
           - La parte después del "@" (dominio) contiene al menos
             un punto "."
           - La parte después del último punto no está vacía
             (la extensión no puede estar vacía)
           - No empieza ni termina con "@"
       * Ejemplos válidos:   "user@example.com", "a@b.c"
       * Ejemplos inválidos: "user@", "@example.com",
                             "user@example", "user@@example.com"
   - mensaje_error():
       * Retorna: "El formato de email no es válido"

5. ReglaNoEspacios(Regla)
   - validar(valor):
       * Retorna True si el valor NO contiene espacios.
   - mensaje_error():
       * Retorna: "El valor no puede contener espacios"

6. Validador
   - Constructor: __init__(self)
       * Inicializa una lista interna vacía de reglas.
   - Métodos:
       * agregar_regla(regla: Regla) -> None
           - Agrega una regla a la lista interna.
           - Si no es instancia de Regla, lanza TypeError("Se requiere instancia de Regla")
       * validar(valor: str) -> dict
           - Ejecuta TODAS las reglas contra el valor.
           - Retorna un diccionario con esta estructura EXACTA:
               {
                   "es_valido": bool,      # True solo si TODAS las reglas pasan
                   "errores": list         # Lista de mensajes de error de las reglas que fallaron
               }
           - Si todas pasan, "errores" es una lista vacía [].
       * cantidad_reglas() -> int
           - Retorna la cantidad de reglas agregadas.

## EJEMPLO

```python
>>> from validador import *
>>> v = Validador()
>>> v.agregar_regla(ReglaLongitud(3, 50))
>>> v.agregar_regla(ReglaNoPalabrasProhibidas())
>>> v.agregar_regla(ReglaFormatoEmail())
>>> v.validar("user@example.com")
{"es_valido": True, "errores": []}

>>> v.validar("ad")
{"es_valido": False, "errores": ["La longitud debe estar entre 3 y 50", "El formato de email no es válido"]}
```

# NOTAS

- No modifiques el archivo de tests.

- Te doy una pista:

```python
from abc import ABC, abstractmethod


class Regla(ABC):
    @abstractmethod
    def validar(self, valor: str) -> bool:
        """Retorna True si el valor cumple la regla."""
        pass

    @abstractmethod
    def mensaje_error(self) -> str:
        """Retorna el mensaje de error de esta regla."""
        pass
```

- Revisa detenidamente los tests para obtener mas detalles de implementación.

- El archivo debe llamarse `validador.py`.
