from src.models.composicion.comedor import Comedor as ComedorCompleto
from src.models.concretos.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedorConcreto:
    def test_agrega_quita_y_cuenta_sillas(self):
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        silla = Silla("Silla", "Madera", "Natural", 50.0)
        comedor = Comedor(mesa)

        comedor.agregar_silla(silla)
        comedor.agregar_silla(silla)

        assert comedor.cantidad_sillas() == 2
        comedor.quitar_silla(silla)
        assert comedor.cantidad_sillas() == 1
        comedor.quitar_silla(Silla("Otra", "Metal", "Negro", 50.0))
        assert comedor.cantidad_sillas() == 1

    def test_calcula_precio_y_descripcion(self):
        mesa = Mesa("Mesa", "Madera", "Natural", 200.0)
        silla = Silla("Silla", "Madera", "Natural", 50.0)
        comedor = Comedor(mesa, [silla])

        assert comedor.calcular_precio_total() == 264.6
        descripcion = comedor.descripcion()
        assert "Comedor con mesa:" in descripcion
        assert "y 1 sillas:" in descripcion
        assert "1. Silla: Silla" in descripcion
