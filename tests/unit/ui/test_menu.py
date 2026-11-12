from unittest.mock import Mock, patch

from src.ui.menu import MenuTienda


class TestMenuTienda:
    def crear_menu(self, inventario=None, comedores=None):
        tienda = Mock()
        tienda.nombre = "Tienda Test"
        tienda._inventario = inventario or []
        tienda._comedores = comedores or []
        return MenuTienda(tienda)

    def test_mostrar_catalogo_maneja_inventario_vacio(self):
        menu = self.crear_menu()

        with patch.object(menu.console, "print") as imprimir:
            menu.mostrar_catalogo_completo()

        imprimir.assert_called_once()

    def test_mostrar_catalogo_muestra_muebles_y_errores(self):
        correcto = Mock(nombre="Silla", material="Madera", color="Negro")
        correcto.calcular_precio.return_value = 75.0
        con_error = Mock(nombre="Mueble inválido", material="Metal", color="Gris")
        con_error.calcular_precio.side_effect = RuntimeError("fallo")
        menu = self.crear_menu([correcto, con_error])

        with patch.object(menu.console, "print") as imprimir:
            menu.mostrar_catalogo_completo()

        imprimir.assert_called_once()

    def test_busqueda_interactiva_maneja_termino_vacio(self):
        menu = self.crear_menu()

        with patch("src.ui.menu.Prompt.ask", return_value="   "), patch.object(
            menu.console, "print"
        ) as imprimir:
            menu.buscar_muebles_interactivo()

        imprimir.assert_called_once()

    def test_busqueda_interactiva_muestra_resultados(self):
        mueble = Mock()
        menu = self.crear_menu()
        menu.tienda.buscar_muebles_por_nombre.return_value = [mueble]

        with patch("src.ui.menu.Prompt.ask", return_value="silla"), patch(
            "src.ui.menu.time.sleep"
        ), patch.object(menu, "_mostrar_lista_muebles") as mostrar:
            menu.buscar_muebles_interactivo()

        mostrar.assert_called_once_with([mueble])

    def test_filtros_interactivos_manejan_rangos_y_material(self):
        menu = self.crear_menu()
        menu.tienda.filtrar_por_precio.return_value = []
        menu.tienda.filtrar_por_material.return_value = []

        with patch("src.ui.menu.IntPrompt.ask", side_effect=[100, 50]), patch.object(
            menu.console, "print"
        ):
            menu.filtrar_por_precio_interactivo()

        with patch("src.ui.menu.Prompt.ask", return_value="   "), patch.object(
            menu.console, "print"
        ):
            menu.filtrar_por_material_interactivo()

    def test_mostrar_comedores_y_estadisticas(self):
        comedor = Mock()
        comedor.obtener_descripcion_completa.return_value = "Descripción"
        menu = self.crear_menu(comedores=[comedor])
        menu.tienda.obtener_estadisticas.return_value = {
            "total_muebles": 1,
            "total_comedores": 1,
            "valor_inventario": 100.0,
            "ventas_realizadas": 0,
            "descuentos_activos": {},
            "total_muebles_vendidos": 0,
            "valor_total_ventas": 0.0,
            "tipos_muebles": {"Silla": 1},
        }

        with patch.object(menu.console, "print"), patch("src.ui.menu.time.sleep"):
            menu.mostrar_comedores()
            menu.mostrar_estadisticas()

        comedor.obtener_descripcion_completa.assert_called_once_with()

    def test_utilidades_de_presentacion(self):
        menu = self.crear_menu()
        venta = {
            "cliente": "Ana",
            "mueble": "Silla",
            "precio_original": 100.0,
            "descuento": 10.0,
            "precio_final": 90.0,
        }

        with patch.object(menu.console, "print") as imprimir:
            menu.mostrar_banner()
            menu._mostrar_comprobante_venta(venta)
            menu._mostrar_lista_muebles([], numerada=True)

        assert imprimir.call_count == 4

    def test_menu_principal_devuelve_opcion_y_ejecutar_puede_salir(self):
        menu = self.crear_menu()

        with patch("src.ui.menu.IntPrompt.ask", return_value=0), patch.object(
            menu.console, "clear"
        ), patch.object(menu.console, "print"):
            assert menu.mostrar_menu_principal() == 0
            menu.ejecutar()

        assert menu.running is False
