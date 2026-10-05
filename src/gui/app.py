"""
Aplicación principal de EsSaludManager.
"""

from src.gui.ventanas.ventana_login import VentanaLogin
from src.gui.ventanas.ventana_principal import VentanaPrincipal


class App:
    """Controla el flujo principal de la aplicación."""

    def __init__(self) -> None:
        """Inicializa la aplicación."""
        self._ventana_login: VentanaLogin | None = None
        self._ventana_principal: VentanaPrincipal | None = None

    def run(self) -> None:
        """Muestra la ventana de inicio de sesión."""
        self._ventana_login = VentanaLogin(
            al_iniciar_sesion=self._abrir_ventana_principal,
        )
        self._ventana_login.mainloop()

    def _abrir_ventana_principal(
        self,
        usuario: dict[str, object],
    ) -> None:
        """
        Abre la ventana principal tras autenticar.

        Args:
            usuario: Datos del usuario autenticado.
        """
        self._ventana_principal = VentanaPrincipal(usuario)
        self._ventana_principal.mainloop()
