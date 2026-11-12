import pytest

from src.models.categorias.superficies import Superficie


class SuperficieDePrueba(Superficie):
    def calcular_precio(self):
        return self.precio_base

    def obtener_descripcion(self):
        return self.obtener_info_superficie()


class TestSuperficie:
    @pytest.fixture
    def superficie(self):
        return SuperficieDePrueba(
            "Superficie",
            "Madera",
            "Natural",
            200.0,
            largo=120.0,
            ancho=80.0,
            altura=75.0,
        )

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Superficie("Superficie", "Madera", "Natural", 200.0, 120, 80, 75)

    def test_calcula_area_factor_y_descripcion(self, superficie):
        assert superficie.calcular_area() == 9600.0
        assert superficie.calcular_factor_tamaño() == pytest.approx(1.048)
        assert superficie.obtener_info_superficie() == (
            "Dimensiones: 120.0x80.0x75.0cm (Área: 9600.0cm²)"
        )

    @pytest.mark.parametrize(
        ("propiedad", "valor"),
        [("largo", 0), ("ancho", -1), ("altura", 0)],
    )
    def test_dimensiones_rechazan_valores_no_positivos(
        self, superficie, propiedad, valor
    ):
        with pytest.raises(ValueError):
            setattr(superficie, propiedad, valor)

    def test_dimensiones_aceptan_valores_positivos(self, superficie):
        superficie.largo = 150
        superficie.ancho = 90
        superficie.altura = 80

        assert superficie.calcular_area() == 13500
