"""
EcoBot — interfaz web (Streamlit) para el agente EcoMarket (Fase 4).
"""

from __future__ import annotations

import time
from typing import Any
from uuid import UUID

from dotenv import load_dotenv
import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama

from agente_ecomarket import CHAT_MODEL, NUM_CTX, construir_agente
from tools import (
    build_consultar_politicas_ecomarket,
    consultar_informacion_pedido,
    generar_etiqueta_devolucion,
)


class _InvokeTimingHandler(BaseCallbackHandler):
    """Mide tiempo por tool y por invocación al modelo de chat (LLM)."""

    def __init__(self) -> None:
        super().__init__()
        self._tool_starts: dict[UUID, tuple[str, float]] = {}
        self.duraciones_tools_s: list[float] = []
        self._llm_starts: dict[UUID, float] = {}
        self.duraciones_llm_s: list[float] = []

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[Any]],
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        self._llm_starts[run_id] = time.perf_counter()

    def on_chat_model_end(self, response: Any, *, run_id: UUID, **kwargs: Any) -> None:
        if run_id not in self._llm_starts:
            return
        t0 = self._llm_starts.pop(run_id)
        self.duraciones_llm_s.append(time.perf_counter() - t0)

    def on_chat_model_error(
        self, error: BaseException, *, run_id: UUID, **kwargs: Any
    ) -> None:
        if run_id not in self._llm_starts:
            return
        t0 = self._llm_starts.pop(run_id)
        self.duraciones_llm_s.append(time.perf_counter() - t0)

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        nombre = serialized.get("name") or "?"
        self._tool_starts[run_id] = (nombre, time.perf_counter())

    def on_tool_end(self, output: Any, *, run_id: UUID, **kwargs: Any) -> None:
        fin = time.perf_counter()
        if run_id not in self._tool_starts:
            return
        _nombre, t0 = self._tool_starts.pop(run_id)
        self.duraciones_tools_s.append(fin - t0)

    def on_tool_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
        fin = time.perf_counter()
        if run_id not in self._tool_starts:
            return
        _nombre, t0 = self._tool_starts.pop(run_id)
        self.duraciones_tools_s.append(fin - t0)


def _asignar_duraciones_tools(tools_list: list[dict], duraciones_s: list[float]) -> None:
    """Fusiona por orden de finalización (coincide con el orden habitual en ReAct)."""
    for i, tool_info in enumerate(tools_list):
        if i < len(duraciones_s):
            tool_info["duracion_s"] = round(duraciones_s[i], 3)
        else:
            tool_info["duracion_s"] = None


def _metricas_llm_turno(handler: _InvokeTimingHandler) -> tuple[float | None, int]:
    """Suma de tiempos del modelo en el turno y número de invocaciones."""
    if not handler.duraciones_llm_s:
        return None, 0
    total = round(sum(handler.duraciones_llm_s), 3)
    return total, len(handler.duraciones_llm_s)


def _render_panel_debug_turno(turno: dict) -> None:
    """Métricas LLM + expander de tools (solo con modo debug activo en la app)."""
    llm_s = turno.get("llm_tiempo_s")
    n = int(turno.get("llm_invocaciones") or 0)
    if llm_s is not None:
        if n > 1:
            st.caption(
                f"Tiempo modelo (LLM), suma de {n} invocaciones: **{llm_s:.3f} s**"
            )
        else:
            st.caption(f"Tiempo modelo (LLM): **{llm_s:.3f} s**")
    else:
        st.caption("Tiempo modelo (LLM): _no disponible_")
    tools = turno.get("tools") or []
    if tools:
        _render_tools_expanders(tools)


def _extraer_tools(mensajes: list) -> list[dict]:
    """Empareja AIMessage.tool_calls con ToolMessage por tool_call_id."""
    resultados = {
        m.tool_call_id: m.content
        for m in mensajes
        if isinstance(m, ToolMessage)
    }
    out: list[dict] = []
    for m in mensajes:
        if not isinstance(m, AIMessage):
            continue
        tool_calls = getattr(m, "tool_calls", None) or []
        for tc in tool_calls:
            tid = tc.get("id")
            nombre = tc.get("name", "")
            args = tc.get("args", {})
            raw = resultados.get(tid, "(sin resultado)")
            resultado = raw if isinstance(raw, str) else str(raw)
            out.append({"nombre": nombre, "args": args, "resultado": resultado})
    return out


def _render_tools_expanders(tools_list: list[dict]) -> None:
    if not tools_list:
        return
    with st.expander("Tools invocadas en este turno"):
        for t in tools_list:
            st.markdown(f"**{t['nombre']}**")
            ds = t.get("duracion_s")
            if ds is not None:
                st.caption(f"Tiempo de ejecución: **{ds:.3f} s**")
            else:
                st.caption("Tiempo de ejecución: _no disponible_")
            st.json(t["args"])
            res = t["resultado"]
            preview = res if len(res) <= 1500 else res[:1500] + "…"
            st.code(preview, language="json")


@st.cache_resource(show_spinner="Inicializando RAG y agente...")
def cargar_agente():
    load_dotenv()
    llm = ChatOllama(model=CHAT_MODEL, temperature=0, num_ctx=NUM_CTX)
    consultar_politicas = build_consultar_politicas_ecomarket()
    tools = [
        consultar_informacion_pedido,
        consultar_politicas,
        generar_etiqueta_devolucion,
    ]
    return construir_agente(llm, tools)


st.set_page_config(page_title="EcoBot — EcoMarket", layout="centered")

agente = cargar_agente()

with st.sidebar:
    st.header("EcoBot")
    st.caption(f"Modelo: {CHAT_MODEL}")
    modo_debug = st.toggle("Modo debug (mostrar tools)", value=False)
    if st.button("Reiniciar conversacion"):
        st.session_state.historial = []
        st.session_state.turnos = []
        st.rerun()

if "historial" not in st.session_state:
    st.session_state.historial = []
if "turnos" not in st.session_state:
    st.session_state.turnos = []

st.title("EcoBot")
st.caption("Asistente de atención al cliente EcoMarket")

for turno in st.session_state.turnos:
    with st.chat_message(turno["role"]):
        st.markdown(turno["content"])
        if modo_debug and turno["role"] == "assistant":
            _render_panel_debug_turno(turno)

entrada = st.chat_input("Escribe tu consulta...")

if entrada:
    st.session_state.historial.append(HumanMessage(content=entrada))
    st.session_state.turnos.append({"role": "user", "content": entrada})

    with st.chat_message("user"):
        st.markdown(entrada)

    with st.chat_message("assistant"):
        timing_cb = _InvokeTimingHandler()
        with st.spinner("Pensando..."):
            estado = agente.invoke(
                {"messages": st.session_state.historial},
                config={"callbacks": [timing_cb]},
            )
        mensajes = estado["messages"]
        ultimo = mensajes[-1]
        respuesta = ""
        if isinstance(ultimo, AIMessage) and ultimo.content:
            respuesta = ultimo.content
        if not respuesta:
            for m in reversed(mensajes):
                if isinstance(m, AIMessage) and m.content:
                    respuesta = m.content
                    break
        tools_usadas = _extraer_tools(mensajes)
        _asignar_duraciones_tools(tools_usadas, timing_cb.duraciones_tools_s)
        llm_total_s, llm_n = _metricas_llm_turno(timing_cb)
        st.markdown(respuesta or "_Sin respuesta de texto._")
        if modo_debug:
            turno_debug = {
                "llm_tiempo_s": llm_total_s,
                "llm_invocaciones": llm_n,
                "tools": tools_usadas,
            }
            _render_panel_debug_turno(turno_debug)

    st.session_state.historial.append(AIMessage(content=respuesta))
    st.session_state.turnos.append(
        {
            "role": "assistant",
            "content": respuesta,
            "tools": tools_usadas,
            "llm_tiempo_s": llm_total_s,
            "llm_invocaciones": llm_n,
        }
    )
