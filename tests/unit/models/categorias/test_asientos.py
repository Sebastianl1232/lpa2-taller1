import pytest

from src.models.categorias.asientos import Asiento


class AsientoDePrueba(Asiento):
    def calcular_precio(self):
        return self.precio_base

    def obtener_descripcion(self):
        return self.obtener_info_asiento()


class TestAsiento:
    @pytest.fixture
    def asiento(self):
        return AsientoDePrueba(
            "Asiento",
            "Madera",
            "Negro",
            100.0,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado="Cuero",
        )

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Asiento("Asiento", "Madera", "Negro", 100.0, 1, True)

    def test_calcula_factor_de_comodidad(self, asiento):
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.4)
        assert asiento.obtener_info_asiento() == (
            "Capacidad: 3 personas, Respaldo: Sí, Tapizado: Cuero"
        )

    def test_propiedades_validan_la_capacidad(self, asiento):
        asiento.capacidad_personas = 4
        asiento.material_tapizado = "Tela"
        asiento.tiene_respaldo = False

        assert asiento.capacidad_personas == 4
        assert asiento.material_tapizado == "Tela"
        assert asiento.tiene_respaldo is False

        with pytest.raises(ValueError):
            asiento.capacidad_personas = 0

    @pytest.mark.parametrize(
        ("respaldo", "tapizado", "capacidad", "factor"),
        [
            (False, None, 1, 1.0),
            (True, "Tela", 2, 1.25),
            (True, "Otro", 4, 1.25),
        ],
    )
    def test_factor_cubre_variantes(
        self, respaldo, tapizado, capacidad, factor
    ):
        asiento = AsientoDePrueba(
            "Asiento",
            "Madera",
            "Negro",
            100.0,
            capacidad,
            respaldo,
            tapizado,
        )

        assert asiento.calcular_factor_comodidad() == pytest.approx(factor)
