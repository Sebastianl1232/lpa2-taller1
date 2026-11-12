from unittest.mock import Mock, patch

from src import main


class TestFuncionesIniciales:
    def test_crear_catalogo_inicial_agrega_todos_los_muebles(self):
        tienda = Mock()
        tienda.agregar_mueble.return_value = "agregado"

        with patch("builtins.print"):
            main.crear_catalogo_inicial(tienda)

        assert tienda.agregar_mueble.call_count == 17

    def test_crear_comedores_ejemplo_agrega_dos_comedores(self):
        tienda = Mock()
        tienda.agregar_comedor.return_value = "agregado"

        with patch("builtins.print"):
            main.crear_comedores_ejemplo(tienda)

        assert tienda.agregar_comedor.call_count == 2
        comedores = [llamada.args[0] for llamada in tienda.agregar_comedor.call_args_list]
        assert [comedor.nombre for comedor in comedores] == [
            "Comedor Familiar Completo",
            "Comedor Moderno Premium",
        ]

    def test_aplicar_descuentos_ejemplo_aplica_tres_descuentos(self):
        tienda = Mock()
        tienda.aplicar_descuento.return_value = "aplicado"

        with patch("builtins.print"):
            main.aplicar_descuentos_ejemplo(tienda)

        assert tienda.aplicar_descuento.call_args_list == [
            (("silla", 10),),
            (("mesa", 15),),
            (("sofa", 20),),
        ]

    def test_mostrar_estadisticas_iniciales_consulta_tienda(self):
        tienda = Mock()
        tienda.obtener_estadisticas.return_value = {
            "total_muebles": 2,
            "total_comedores": 1,
            "valor_inventario": 500.0,
            "descuentos_activos": {"Silla": 0.1},
            "ventas_realizadas": 0,
            "total_muebles_vendidos": 0,
            "valor_total_ventas": 0.0,
            "tipos_muebles": {"Silla": 2},
        }

        with patch("builtins.print"):
            main.mostrar_estadisticas_iniciales(tienda)

        tienda.obtener_estadisticas.assert_called_once_with()
