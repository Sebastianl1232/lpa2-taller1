from unittest.mock import Mock

import pytest

from src.services.tienda import TiendaMuebles


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

    def test_buscar_y_filtrar_inventario(self, tienda_vacia):
        silla = Mock(nombre="Silla de madera", material="Madera")
        silla.calcular_precio.return_value = 75.0
        mesa = Mock(nombre="Mesa de vidrio", material="Vidrio")
        mesa.calcular_precio.return_value = 200.0
        tienda_vacia._inventario = [silla, mesa]

        assert tienda_vacia.buscar_muebles_por_nombre("  SILLA ") == [silla]
        assert tienda_vacia.buscar_muebles_por_nombre("   ") == []
        assert tienda_vacia.filtrar_por_precio(70, 100) == [silla]
        assert tienda_vacia.filtrar_por_material(" madera ") == [silla]
        assert tienda_vacia.filtrar_por_material("") == []

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
