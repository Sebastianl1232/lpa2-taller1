import pytest

from src.models.categorias.almacenamiento import Almacenamiento


class AlmacenamientoDePrueba(Almacenamiento):
    def calcular_precio(self):
        return self.precio_base

    def obtener_descripcion(self):
        return self.obtener_info_almacenamiento()


class TestAlmacenamiento:
    @pytest.fixture
    def almacenamiento(self):
        return AlmacenamientoDePrueba(
            "Almacenamiento",
            "Madera",
            "Blanco",
            500.0,
            num_compartimentos=4,
            capacidad_litros=250.0,
        )

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Almacenamiento(
                "Almacenamiento",
                "Madera",
                "Blanco",
                500.0,
                4,
                250.0,
            )

    def test_calcula_factor_y_obtiene_informacion(self, almacenamiento):
        assert almacenamiento.calcular_factor_almacenamiento() == 1.2
        assert almacenamiento.obtener_info_almacenamiento() == (
            "Compartimentos: 4, Capacidad: 250.0L"
        )

    @pytest.mark.parametrize(
        ("propiedad", "valor"),
        [("num_compartimentos", 0), ("capacidad_litros", -1)],
    )
    def test_propiedades_rechazan_valores_no_positivos(
        self, almacenamiento, propiedad, valor
    ):
        with pytest.raises(ValueError):
            setattr(almacenamiento, propiedad, valor)

    def test_propiedades_aceptan_valores_positivos(self, almacenamiento):
        almacenamiento.num_compartimentos = 6
        almacenamiento.capacidad_litros = 400

        assert almacenamiento.num_compartimentos == 6
        assert almacenamiento.capacidad_litros == 400
