"""
Tool: consultar_informacion_pedido
Entrada : numero_pedido (str)
Salida  : dict con datos básicos del pedido (cliente, productos, estado, fecha)
          o dict con error si el pedido no existe.
"""

import json
from langchain_core.tools import tool

from data.mock_data import PEDIDOS


@tool
def consultar_informacion_pedido(numero_pedido: str) -> str:
    """Consulta la información básica de un pedido de EcoMarket.

    Devuelve los datos del cliente, lista de productos, estado actual y fecha
    de entrega. Úsala cuando el cliente pregunte por el estado o contenido de
    un pedido antes de iniciar cualquier proceso de devolución.

    Args:
        numero_pedido: Identificador del pedido, por ejemplo 'ECO-PED-0001'.

    Returns:
        JSON con los datos del pedido o un mensaje de error si no se encuentra.
    """
    pedido = PEDIDOS.get(numero_pedido.strip().upper())

    if pedido is None:
        return json.dumps(
            {
                "exito": False,
                "mensaje": (
                    f"No se encontró el pedido '{numero_pedido}'. "
                    "Verifica que el número sea correcto."
                ),
            },
            ensure_ascii=False,
        )

    resultado = {
        "exito": True,
        "numero_pedido": pedido["numero_pedido"],
        "cliente": pedido["cliente"],
        "fecha_compra": pedido["fecha_compra"],
        "fecha_entrega": pedido["fecha_entrega"],
        "estado": pedido["estado"],
        "metodo_pago": pedido["metodo_pago"],
        "productos": pedido["productos"],
        "total_cop": pedido["total"],
    }

    return json.dumps(resultado, ensure_ascii=False, indent=2)
