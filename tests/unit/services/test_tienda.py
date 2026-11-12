from unittest.mock import Mock

import pytest

from src.services.tienda import TiendaMuebles
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestTiendaMuebles:
    @pytest.fixture
    def tienda_vacia(self):
        return TiendaMuebles("Tienda de Pruebas")

    @pytest.fixture
    def silla_mock(self):
        silla = Mock()
        silla.nombre = "Silla Mock"
        silla.material = "Madera"
        silla.calcular_precio.return_value = 75.0
        return silla

    def test_inicializa_tienda_vacia(self, tienda_vacia):
        assert tienda_vacia.nombre == "Tienda de Pruebas"
        assert tienda_vacia._inventario == []
        assert tienda_vacia._comedores == []

    def test_agregar_mueble_retorna_confirmacion(self, tienda_vacia, silla_mock):
        resultado = tienda_vacia.agregar_mueble(silla_mock)

        assert resultado == "Mueble Silla Mock agregado exitosamente al inventario"
        assert tienda_vacia._inventario == [silla_mock]
        silla_mock.calcular_precio.assert_called_once_with()

    @pytest.mark.parametrize(
        ("mueble", "mensaje"),
        [
            (None, "Error: El mueble no puede ser None"),
        ],
    )
    def test_agregar_mueble_rechaza_entrada_invalida(
        self, tienda_vacia, mueble, mensaje
    ):
        assert tienda_vacia.agregar_mueble(mueble) == mensaje

    def test_agregar_mueble_rechaza_precio_no_positivo(self, tienda_vacia):
        mueble = Mock()
        mueble.calcular_precio.return_value = 0

        assert (
            tienda_vacia.agregar_mueble(mueble)
            == "Error: El mueble debe tener un precio válido mayor a 0"
        )
        assert tienda_vacia._inventario == []

    def test_agregar_mueble_reporta_error_de_precio(self, tienda_vacia):
        mueble = Mock()
        mueble.calcular_precio.side_effect = ValueError("precio inválido")

        assert tienda_vacia.agregar_mueble(mueble) == (
            "Error al calcular precio del mueble: precio inválido"
        )

    def test_agregar_comedor_valida_y_agrega(self, tienda_vacia):
        comedor = Mock(nombre="Comedor")

        assert tienda_vacia.agregar_comedor(comedor) == (
            "Comedor Comedor agregado exitosamente"
        )
        assert tienda_vacia._comedores == [comedor]
        assert tienda_vacia.agregar_comedor(None) == "Error: El comedor no puede ser None"

    def test_buscar_y_filtrar_inventario(self, tienda_vacia):
        silla = Mock(nombre="Silla de madera", material="Madera")
        silla.calcular_precio.return_value = 75.0
        mesa = Mock(nombre="Mesa de vidrio", material="Vidrio")
        mesa.calcular_precio.return_value = 200.0
        mueble_con_error = Mock(nombre="Mueble inválido", material="Madera")
        mueble_con_error.calcular_precio.side_effect = RuntimeError("error")
        tienda_vacia._inventario = [silla, mesa, mueble_con_error]

        assert tienda_vacia.buscar_muebles_por_nombre("  SILLA ") == [silla]
        assert tienda_vacia.buscar_muebles_por_nombre("   ") == []
        assert tienda_vacia.filtrar_por_precio(70, 100) == [silla]
        assert tienda_vacia.filtrar_por_material(" madera ") == [
            silla,
            mueble_con_error,
        ]
        assert tienda_vacia.filtrar_por_material("") == []
        assert tienda_vacia.filtrar_por_precio(-10, 100) == [silla]

    def test_aplicar_descuento_normaliza_categoria(self, tienda_vacia):
        resultado = tienda_vacia.aplicar_descuento("sillas", 10)

        assert resultado == "Descuento del 10% aplicado a la categoría 'Silla'"
        assert tienda_vacia._descuentos_activos == {"Silla": 0.1}

    @pytest.mark.parametrize("porcentaje", [0, -1, 101])
    def test_aplicar_descuento_rechaza_porcentaje_invalido(
        self, tienda_vacia, porcentaje
    ):
        assert tienda_vacia.aplicar_descuento("sillas", porcentaje) == (
            "Error: El porcentaje debe estar entre 1 y 100"
        )

    def test_realizar_venta_aplica_descuento_y_actualiza_estado(
        self, tienda_vacia, silla_mock
    ):
        tienda_vacia.agregar_mueble(silla_mock)
        tienda_vacia.aplicar_descuento("mocks", 10)

        resultado = tienda_vacia.realizar_venta(silla_mock, "Ana")

        assert resultado["mueble"] == "Silla Mock"
        assert resultado["cliente"] == "Ana"
        assert resultado["precio_original"] == 75.0
        assert resultado["descuento"] == 10.0
        assert resultado["precio_final"] == 67.5
        assert len(resultado["fecha"]) == 19
        assert resultado["fecha"][4] == "-"
        assert resultado["fecha"][7] == "-"
        assert resultado["fecha"][10] == " "
        assert resultado["fecha"][13] == ":"
        assert resultado["fecha"][16] == ":"
        assert tienda_vacia._inventario == []
        assert tienda_vacia._total_muebles_vendidos == 1
        assert tienda_vacia._valor_total_ventas == 67.5

    def test_realizar_venta_rechaza_mueble_no_disponible(
        self, tienda_vacia, silla_mock
    ):
        assert tienda_vacia.realizar_venta(silla_mock) == {
            "error": "El mueble no está disponible en inventario"
        }

    def test_realizar_venta_reporta_error_de_calculo(self, tienda_vacia):
        mueble = Mock(nombre="Mueble", calcular_precio=Mock(side_effect=RuntimeError("fallo")))
        tienda_vacia._inventario = [mueble]

        assert tienda_vacia.realizar_venta(mueble) == {
            "error": "Error al procesar la venta: fallo"
        }

    def test_estadisticas_y_reporte_reflejan_estado(self, tienda_vacia, silla_mock):
        comedor = Mock()
        comedor.calcular_precio_total.return_value = 300.0
        tienda_vacia.agregar_mueble(silla_mock)
        tienda_vacia.agregar_comedor(comedor)
        tienda_vacia.aplicar_descuento("sillas", 10)

        estadisticas = tienda_vacia.obtener_estadisticas()
        assert estadisticas["total_muebles"] == 1
        assert estadisticas["total_comedores"] == 1
        assert estadisticas["valor_inventario"] == 75.0
        assert estadisticas["tipos_muebles"] == {"Mock": 1}
        assert estadisticas["descuentos_activos"] == {"Silla": 0.1}

        assert tienda_vacia.estadisticas() == estadisticas
        reporte = tienda_vacia.generar_reporte_inventario()
        assert "Total de muebles: 1" in reporte
        assert "Total de comedores: 1" in reporte
        assert "- Mock: 1 unidades" in reporte
        assert "- Silla: 10.0%" in reporte

    def test_obtener_muebles_por_tipo_filtra_instancias(self, tienda_vacia):
        silla = Silla("Silla", "Madera", "Negro", 50.0)
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        tienda_vacia._inventario = [silla, mesa]

        assert tienda_vacia.obtener_muebles_por_tipo(Silla) == [silla]

    def test_calcular_valor_inventario_suma_muebles_y_comedores(
        self, tienda_vacia
    ):
        silla = Silla("Silla", "Madera", "Negro", 50.0)
        comedor = Mock()
        comedor.calcular_precio_total.return_value = 300.0
        tienda_vacia._inventario = [silla]
        tienda_vacia._comedores = [comedor]

        assert tienda_vacia.calcular_valor_inventario() == 355.0

    def test_contar_tipos_muebles(self, tienda_vacia):
        silla = Silla("Silla", "Madera", "Negro", 50.0)
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        tienda_vacia._inventario = [silla, mesa, silla]

        assert tienda_vacia._contar_tipos_muebles() == {
            "Silla": 2,
            "Mesa": 1,
        }
