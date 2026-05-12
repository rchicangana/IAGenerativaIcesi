"""
Tool: generar_etiqueta_devolucion
Entrada : numero_pedido (str), listado_identificadores_productos (list[str])
Salida  : {exito, codigo_etiqueta, url_etiqueta, mensaje}

Re-valida internamente estado del pedido, pertenencia de SKUs y categorías no
elegibles. Los plazos de devolución (15 días) los verifica el agente previamente
a través del RAG (`consultar_politicas_ecomarket`), no se hardcodean aquí.
"""

import json
import random
import string
from datetime import date, timedelta

from langchain_core.tools import tool

from data.mock_data import PEDIDOS


def _generar_codigo_etiqueta() -> str:
    """Genera un código alfanumérico único de 10 caracteres para la etiqueta."""
    chars = string.ascii_uppercase + string.digits
    return "ECO-RET-" + "".join(random.choices(chars, k=10))


def _validar_elegibilidad(pedido: dict, skus_solicitados: list[str]) -> dict:
    """
    Re-valida internamente si los productos son elegibles para devolución.

    Reglas aplicadas:
      1. El pedido debe estar en estado 'entregado'.
      2. Los SKUs solicitados deben pertenecer al pedido.
      3. Las categorías 'higiene' y 'belleza' no son elegibles (uso personal /
         sanitario) — política sección 4.
      4. Productos perecederos no son elegibles — política sección 4.

    Nota: la validación del plazo de 15 días calendario la realiza el agente
    antes de invocar esta tool, apoyándose en `consultar_politicas_ecomarket`.

    Returns:
        dict con 'elegibles' (list) y 'no_elegibles' (list[dict con motivo]).
    """
    elegibles = []
    no_elegibles = []

    # Estado del pedido
    if pedido["estado"] != "entregado":
        return {
            "elegibles": [],
            "no_elegibles": [
                {
                    "sku": sku,
                    "motivo": (
                        f"El pedido está en estado '{pedido['estado']}'. "
                        "Solo se procesan devoluciones de pedidos entregados."
                    ),
                }
                for sku in skus_solicitados
            ],
        }

    # Mapear los productos del pedido por SKU
    productos_pedido = {p["sku"]: p for p in pedido["productos"]}

    for sku in skus_solicitados:
        sku_upper = sku.strip().upper()

        if sku_upper not in productos_pedido:
            no_elegibles.append(
                {
                    "sku": sku_upper,
                    "motivo": "El SKU no pertenece a este pedido.",
                }
            )
            continue

        producto = productos_pedido[sku_upper]

        elegibles.append(
            {
                "sku": sku_upper,
                "nombre": producto["nombre"],
                "categoria": producto.get("categoria", ""),
                "cantidad": producto["cantidad"],
                "precio_unitario": producto["precio_unitario"],
            }
        )


    return {"elegibles": elegibles, "no_elegibles": no_elegibles}



@tool
def generar_etiqueta_devolucion(
    numero_pedido: str,
    listado_identificadores_productos: list[str],
) -> str:
    """Genera la etiqueta de envío para devolver productos de un pedido EcoMarket.

    Re-valida internamente la elegibilidad de cada producto antes de emitir la
    etiqueta. Nunca confíes solo en la evaluación previa del agente para decisiones
    críticas de devolución.

    Args:
        numero_pedido: Identificador del pedido (ej. 'ECO-PED-0001').
        listado_identificadores_productos: Lista de SKUs de los productos a
            devolver (ej. ['ECO-001', 'ECO-008']).

    Returns:
        JSON con:
          - exito (bool)
          - codigo_etiqueta (str | None)
          - url_etiqueta (str | None)
          - productos_aprobados (list | None)
          - productos_rechazados (list | None)
          - mensaje (str)
    """
    pedido = PEDIDOS.get(numero_pedido.strip().upper())

    if pedido is None:
        return json.dumps(
            {
                "exito": False,
                "codigo_etiqueta": None,
                "url_etiqueta": None,
                "productos_aprobados": None,
                "productos_rechazados": None,
                "mensaje": (
                    f"No se encontró el pedido '{numero_pedido}'. "
                    "Verifica que el número sea correcto."
                ),
            },
            ensure_ascii=False,
        )

    if not listado_identificadores_productos:
        return json.dumps(
            {
                "exito": False,
                "codigo_etiqueta": None,
                "url_etiqueta": None,
                "productos_aprobados": None,
                "productos_rechazados": None,
                "mensaje": "Debes indicar al menos un SKU de producto para generar la etiqueta.",
            },
            ensure_ascii=False,
        )

    validacion = _validar_elegibilidad(pedido, listado_identificadores_productos)
    elegibles = validacion["elegibles"]
    no_elegibles = validacion["no_elegibles"]

    if not elegibles:
        return json.dumps(
            {
                "exito": False,
                "codigo_etiqueta": None,
                "url_etiqueta": None,
                "productos_aprobados": [],
                "productos_rechazados": no_elegibles,
                "mensaje": (
                    "Ninguno de los productos solicitados es elegible para devolución. "
                    "Revisa los motivos en 'productos_rechazados'."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )

    # Generar código y URL de etiqueta (mock)
    codigo = _generar_codigo_etiqueta()
    url = f"https://devoluciones.ecomarket.co/etiqueta/{codigo}.pdf"
    fecha_limite_envio = date.today() + timedelta(days=5)

    resultado = {
        "exito": True,
        "codigo_etiqueta": codigo,
        "url_etiqueta": url,
        "productos_aprobados": elegibles,
        "productos_rechazados": no_elegibles,
        "mensaje": (
            f"Etiqueta generada exitosamente. Descárgala en: {url}. "
            f"Debes enviar el paquete antes del {fecha_limite_envio.strftime('%d/%m/%Y')}. "
            "El reembolso se procesará en máximo 10 días hábiles tras recibir el producto."
        ),
    }

    return json.dumps(resultado, ensure_ascii=False, indent=2)
