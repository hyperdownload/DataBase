import logging
import os
import sys

class DynamicLogger:
    def __init__(self, log_file_name: str = "app_log.txt", log_level: int = logging.INFO, log_to_console: bool = False):
        """
        Inicializa el logger con configuraciones dinámicas y maneja automáticamente excepciones no capturadas.

        Parameters:
            log_file_name (str): Nombre del archivo de log.
            log_level (int): Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            log_to_console (bool): Indica si se debe loggear también a la consola.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Evita añadir manejadores duplicados si ya existen
        if not self.logger.handlers:
            # Crear formato de log
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

            # Configuración del archivo de log
            if log_file_name:
                # Crear directorio si no existe
                if not os.path.exists("logs"):
                    os.makedirs("logs")
                file_handler = logging.FileHandler(os.path.join("logs", log_file_name))
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

            # Configuración opcional de la consola
            if log_to_console:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_level)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

        # Redirigir todas las excepciones no capturadas al logger
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Manejador de excepciones global para capturar errores no capturados."""
        if issubclass(exc_type, KeyboardInterrupt):
            # No loguear si se interrumpe manualmente con Ctrl+C
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Registrar el error con traza completa
        self.logger.critical("Excepción no capturada:", exc_info=(exc_type, exc_value, exc_traceback))

    def log(self, level: int, message: str):
        """Registra un mensaje en el nivel especificado."""
        self.logger.log(level, message)

    def debug(self, message: str):
        """Registra un mensaje de depuración."""
        self.logger.debug(message)

    def info(self, message: str):
        """Registra un mensaje informativo."""
        self.logger.info(message)

    def warning(self, message: str):
        """Registra una advertencia."""
        self.logger.warning(message)

    def error(self, message: str):
        """Registra un error."""
        self.logger.error(message)

    def critical(self, message: str):
        """Registra un error crítico."""
        self.logger.critical(message)
