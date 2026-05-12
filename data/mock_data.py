"""
Mock data para el agente EcoMarket.
Simula la base de datos de pedidos y productos.

Nota: las reglas de plazos y condiciones de devolución NO se definen aquí;
el agente las obtiene en tiempo de ejecución desde el RAG
(`consultar_politicas_ecomarket`).
"""

# ---------------------------------------------------------------------------
# Base de datos de pedidos (mock)
# Cada pedido contiene: cliente, productos asociados, estado y fecha.
# ---------------------------------------------------------------------------
PEDIDOS: dict[str, dict] = {
    "ECO-PED-0001": {
        "numero_pedido": "ECO-PED-0001",
        "cliente": {
            "nombre": "María González",
            "email": "maria.gonzalez@email.com",
            "telefono": "3001234567",
        },
        "fecha_compra": "2026-04-27",
        "fecha_entrega": "2026-04-30",
        "estado": "entregado",
        "metodo_pago": "tarjeta_credito",
        "productos": [
            {
                "sku": "ECO-001",
                "nombre": "Botella reutilizable",
                "categoria": "accesorios",
                "cantidad": 1,
                "precio_unitario": 35000,
            },
            {
                "sku": "ECO-008",
                "nombre": "Termo de acero inoxidable",
                "categoria": "accesorios",
                "cantidad": 2,
                "precio_unitario": 68000,
            },
        ],
        "total": 171000,
    },
    "ECO-PED-0002": {
        "numero_pedido": "ECO-PED-0002",
        "cliente": {
            "nombre": "Carlos Ramírez",
            "email": "carlos.ramirez@email.com",
            "telefono": "3109876543",
        },
        "fecha_compra": "2026-05-01",
        "fecha_entrega": "2026-05-04",
        "estado": "entregado",
        "metodo_pago": "contraentrega",
        "productos": [
            {
                "sku": "ECO-004",
                "nombre": "Shampoo solido",
                "categoria": "belleza",
                "cantidad": 1,
                "precio_unitario": 27000,
            },
            {
                "sku": "ECO-005",
                "nombre": "Cepillo dental de bambu",
                "categoria": "higiene",
                "cantidad": 3,
                "precio_unitario": 12000,
            },
            {
                "sku": "ECO-018",
                "nombre": "Pasta dental natural",
                "categoria": "higiene",
                "cantidad": 2,
                "precio_unitario": 21000,
            },
        ],
        "total": 105000,
    },
    "ECO-PED-0003": {
        "numero_pedido": "ECO-PED-0003",
        "cliente": {
            "nombre": "Lucía Herrera",
            "email": "lucia.herrera@email.com",
            "telefono": "3154567890",
        },
        "fecha_compra": "2026-05-05",
        "fecha_entrega": "2026-05-08",
        "estado": "entregado",
        "metodo_pago": "pse",
        "productos": [
            {
                "sku": "ECO-025",
                "nombre": "Set de recipientes de vidrio 3u",
                "categoria": "cocina",
                "cantidad": 1,
                "precio_unitario": 54000,
            },
            {
                "sku": "ECO-096",
                "nombre": "Sarten ceramica libre PFOA",
                "categoria": "cocina",
                "cantidad": 1,
                "precio_unitario": 145000,
            },
        ],
        "total": 199000,
    },
    "ECO-PED-0004": {
        "numero_pedido": "ECO-PED-0004",
        "cliente": {
            "nombre": "Andrés Morales",
            "email": "andres.morales@email.com",
            "telefono": "3207654321",
        },
        "fecha_compra": "2026-05-09",
        "fecha_entrega": "2026-05-11",
        "estado": "entregado",
        "metodo_pago": "tarjeta_debito",
        "productos": [
            {
                "sku": "ECO-074",
                "nombre": "Cargador solar portatil",
                "categoria": "tecnologia",
                "cantidad": 1,
                "precio_unitario": 129000,
            },
        ],
        "total": 129000,
    },
    "ECO-PED-0005": {
        "numero_pedido": "ECO-PED-0005",
        "cliente": {
            "nombre": "Sofía Vargas",
            "email": "sofia.vargas@email.com",
            "telefono": "3002345678",
        },
        "fecha_compra": "2026-05-10",
        "fecha_entrega": None,
        "estado": "en_camino",
        "metodo_pago": "tarjeta_credito",
        "productos": [
            {
                "sku": "ECO-083",
                "nombre": "Mat de yoga corcho",
                "categoria": "bienestar",
                "cantidad": 1,
                "precio_unitario": 95000,
            },
            {
                "sku": "ECO-084",
                "nombre": "Bloque yoga corcho 2u",
                "categoria": "bienestar",
                "cantidad": 1,
                "precio_unitario": 48000,
            },
        ],
        "total": 143000,
    },
}
