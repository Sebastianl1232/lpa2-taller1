import pytest

from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedor:
    @pytest.fixture
    def mesa(self):
        return Mesa(
            "Mesa Comedor",
            "Roble",
            "Natural",
            200.0,
            largo=120.0,
            ancho=80.0,
            capacidad_personas=4,
        )

    @pytest.fixture
    def sillas(self):
        return [
            Silla(
                "Silla Comedor",
                "Roble",
                "Natural",
                50.0,
                material_tapizado="Tela",
            )
            for _ in range(4)
        ]

    @pytest.fixture
    def comedor_completo(self, mesa, sillas):
        return Comedor("Comedor Familiar", mesa, sillas)

    def test_composicion_conserva_mesa_y_sillas(self, comedor_completo, mesa, sillas):
        assert comedor_completo.nombre == "Comedor Familiar"
        assert comedor_completo.mesa is mesa
        assert comedor_completo.sillas == sillas
        assert all(isinstance(silla, Silla) for silla in comedor_completo.sillas)
        assert len(comedor_completo) == 5

    def test_sillas_devuelve_una_copia(self, comedor_completo):
        sillas = comedor_completo.sillas
        sillas.clear()

        assert len(comedor_completo.sillas) == 4

    def test_calcular_precio_total_aplica_descuento_de_set(
        self, comedor_completo
    ):
        precio_sin_descuento = 209.6 + (4 * 60.0)

        assert comedor_completo.calcular_precio_total() == round(
            precio_sin_descuento * 0.95, 2
        )

    def test_agregar_silla_y_respetar_capacidad_maxima(self, mesa):
        comedor = Comedor("Comedor", mesa)

        for numero in range(4):
            resultado = comedor.agregar_silla(
                Silla(f"Silla {numero}", "Roble", "Natural", 50.0)
            )
            assert "agregada exitosamente" in resultado

        resultado = comedor.agregar_silla(Silla("Silla extra", "Roble", "Natural", 50.0))

        assert resultado == "No se pueden agregar más sillas. Capacidad máxima: 4"
        assert len(comedor.sillas) == 4

    def test_agregar_silla_rechaza_tipo_incorrecto(self, comedor_completo):
        resultado = comedor_completo.agregar_silla("No es una silla")

        assert resultado == "Error: Solo se pueden agregar objetos de tipo Silla"
        assert len(comedor_completo.sillas) == 4

    def test_quitar_silla_por_indice(self, comedor_completo):
        resultado = comedor_completo.quitar_silla(0)

        assert resultado == "Silla Silla Comedor removida del comedor"
        assert len(comedor_completo.sillas) == 3

    def test_quitar_silla_maneja_lista_vacia_e_indice_invalido(self, mesa):
        comedor = Comedor("Comedor", mesa)

        assert comedor.quitar_silla() == "No hay sillas para quitar"

        comedor.agregar_silla(Silla("Silla", "Roble", "Natural", 50.0))
        assert comedor.quitar_silla(3) == "Índice de silla inválido"
        assert len(comedor.sillas) == 1

    def test_resumen_incluye_componentes_y_materiales(self, comedor_completo):
        resumen = comedor_completo.obtener_resumen()

        assert resumen["nombre"] == "Comedor Familiar"
        assert resumen["total_muebles"] == 5
        assert resumen["precio_mesa"] == 209.6
        assert resumen["precio_sillas"] == 240.0
        assert resumen["precio_total"] == 427.12
        assert resumen["capacidad_personas"] == 4
        assert set(resumen["materiales_utilizados"]) == {"Roble", "Tela"}

    def test_descripcion_completa_incluye_descuento(self, comedor_completo):
        descripcion = comedor_completo.obtener_descripcion_completa()

        assert "=== COMEDOR COMEDOR FAMILIAR ===" in descripcion
        assert "SILLAS (4 unidades):" in descripcion
        assert "--- PRECIO TOTAL: $427.12 ---" in descripcion
        assert "Incluye 5% de descuento por set completo" in descripcion

    def test_descripcion_sin_sillas(self, mesa):
        comedor = Comedor("Comedor Vacío", mesa)

        assert "SILLAS: Ninguna incluida" in comedor.obtener_descripcion_completa()
        assert str(comedor) == "Comedor Comedor Vacío: Mesa + 0 sillas"
