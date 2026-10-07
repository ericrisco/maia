# Maia Knowledge

Entrena respuestas factuales y naturales sobre Andorra a partir de `docs/temes/`.

- `examples/`: pocas conversaciones para calibrar tono y calidad.
- `review/`: registros aceptados después de comprobar diálogo y fuentes.
- `output/`: exportaciones regenerables para entrenamiento.
- `reports/`: cobertura y controles de calidad.

Las fuentes y notas de revisión se guardan aparte. El JSONL de entrenamiento
solo contiene mensajes `user` y `assistant`.
