from agent_observatory.exporters import ConsoleExporter, Exporter

# NOTE:
# This file demonstrates exporter neutrality.
# Agent and runtime code do not change when exporters change.


def build_exporter() -> Exporter | list[Exporter]:
    exporters: list[Exporter] = [
        ConsoleExporter(),
        # Additional exporters (e.g. OTEL) can be added here
        # without modifying agent or runtime code.
    ]

    if len(exporters) == 1:
        return exporters[0]

    return exporters
