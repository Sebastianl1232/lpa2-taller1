import pytest

from src.models.mueble import Mueble


class MuebleDePrueba(Mueble):
    def calcular_precio(self):
        return self.precio_base

    def obtener_descripcion(self):
        return str(self)


class TestMueble:
    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Mueble("Mesa", "Madera", "Natural", 100.0)

    def test_tiene_metodos_abstractos(self):
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__

    def test_propiedades_validas_se_actualizan(self):
        mueble = MuebleDePrueba("Mesa", "Madera", "Natural", 100.0)

        mueble.nombre = "  Escritorio  "
        mueble.material = "  Roble  "
        mueble.color = "  Blanco  "
        mueble.precio_base = 125.0

        assert mueble.nombre == "Escritorio"
        assert mueble.material == "Roble"
        assert mueble.color == "Blanco"
        assert mueble.precio_base == 125.0

    @pytest.mark.parametrize(
        ("propiedad", "valor"),
        [
            ("nombre", ""),
            ("nombre", "   "),
            ("material", ""),
            ("material", "   "),
            ("color", ""),
            ("color", "   "),
        ],
    )
    def test_propiedades_textuales_rechazan_valores_vacios(
        self, propiedad, valor
    ):
        mueble = MuebleDePrueba("Mesa", "Madera", "Natural", 100.0)

        with pytest.raises(ValueError):
            setattr(mueble, propiedad, valor)

    def test_precio_base_rechaza_valores_negativos(self):
        mueble = MuebleDePrueba("Mesa", "Madera", "Natural", 100.0)

        with pytest.raises(ValueError):
            mueble.precio_base = -1.0

    def test_representaciones_textuales(self):
        mueble = MuebleDePrueba("Mesa", "Madera", "Natural", 100.0)

        assert str(mueble) == "Mesa de Madera en color Natural"
        assert repr(mueble) == (
            "Mueble(nombre='Mesa', material='Madera', "
            "color='Natural', precio_base=100.0)"
        )
