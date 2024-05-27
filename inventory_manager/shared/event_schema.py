PedidoCreado = {
    "type": "object",
    "properties": {
        "idPedido": {"type": "string"},
        "fechaPedido": {"type": "string", "format": "date-time"},
        "clienteId": {"type": "string"},
        "productos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "productoId": {"type": "string"},
                    "cantidad": {"type": "integer"}
                }
            }
        },
        "total": {"type": "number"}
    },
    "required": ["idPedido", "fechaPedido", "clienteId", "productos", "total"]
}

InventarioActualizado = {
    "type": "object",
    "properties": {
        "fechaActualizacion": {"type": "string", "format": "date-time"},
        "productosActualizados": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "productoId": {"type": "string"},
                    "cantidadActual": {"type": "integer"}
                }
            }
        }
    },
    "required": ["fechaActualizacion", "productosActualizados"]
}
