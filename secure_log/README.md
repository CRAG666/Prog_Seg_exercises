# Sistema de Registro de Eventos (Log Seguro) Prog_Seg_exercises

## DESCRIPCIÓN

Debes implementar un sistema de registro de eventos de seguridad. Este tipo de sistema es fundamental en ciberseguridad para auditar y monitorear actividades.


## TIPOS DE EVENTOS VÁLIDOS


| Tipo de evento | Descripción                     |
| -------------- | ------------------------------- |
| `LOGIN`        | El usuario inició sesión        |
| `LOGOUT`       | El usuario cerró sesión         |
| `ERROR`        | Ocurrió un error en el sistema  |
| `ALERTA`       | Se detectó actividad sospechosa |


Cualquier otro tipo de evento es INVÁLIDO.

## CLASES QUE DEBES IMPLEMENTAR

1. Evento
   - Atributos privados: __tipo, __mensaje, __timestamp
   - Constructor: __init__(self, tipo: str, mensaje: str)
       * __tipo      : str, debe ser uno de los tipos válidos.
                       Si el tipo NO es válido, lanza ValueError.
       * __mensaje   : str, descripción del evento.
                       Si está vacío o es solo espacios, lanza ValueError.
       * __timestamp : float, se genera automáticamente con time.time()
                       (NO lo recibe como parámetro)
   - Métodos:
       * get_tipo()       -> str
       * get_mensaje()    -> str
       * get_timestamp()  -> float

2. RegistradorSeguro
   - Atributo privado: __eventos (lista de objetos Evento)
   - Constructor: __init__(self)
       * Inicializa __eventos como lista vacía
   - Métodos:
       * registrar(evento: Evento) -> bool
           - Agrega el evento a la lista interna.
           - Retorna True si fue agregado exitosamente.
           - Retorna False si el parámetro no es una instancia de Evento.
       * obtener_eventos() -> list
           - Retorna una COPIA de la lista de eventos.
       * filtrar_por_tipo(tipo: str) -> list
           - Retorna una nueva lista con solo los eventos
             cuyo tipo coincide con el parámetro.
           - Si no hay eventos de ese tipo, retorna lista vacía.
       * cantidad_eventos() -> int
           - Retorna la cantidad total de eventos registrados.
       * cantidad_por_tipo(tipo: str) -> int
           - Retorna cuántos eventos hay de un tipo dado.
       * ultimo_evento() -> Evento o None
           - Retorna el último evento registrado.
           - Retorna None si no hay eventos.
       * limpiar() -> None
           - Elimina todos los eventos registrados.

## Esturctura

Nombre del archivo: `log.py`

Recuerda revisar los tests para mas detalles de implementación.
