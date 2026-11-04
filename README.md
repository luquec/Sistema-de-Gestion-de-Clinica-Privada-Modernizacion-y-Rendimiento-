
# Sistema de Gestión Clínica: Laboratorio de Rendimiento y Algoritmos

Este proyecto implementa un **sistema de gestión a gran escala para una clínica privada en Python**. Su objetivo principal es justificar la selección de estructuras de datos y algoritmos mediante **evidencia empírica de rendimiento (tiempo y memoria RAM)**, utilizando conjuntos de datos desordenados generados programáticamente (desde 500 hasta 200,000 registros).

---

## Entidades del Sistema
*   **Paciente:** Cédula, nombre, edad, fecha de registro, nivel de prioridad (1-crítico, 2-urgente, 3-normal) y tipo de sangre.
*   **Consulta:** ID de consulta, cédula del paciente, fecha, diagnóstico y gravedad (1-3).
*   **Diagnóstico:** Código, área médica, especialidad y diagnóstico específico.

---

## Módulos Implementados

### Módulo 1 — Estructura de Atención (Cola con Prioridad)
*   **Gestión de Emergencias:** Flujo de pacientes priorizado en tiempo real (prioridad 1 a 3).
*   **Simulación Dinámica:** Registro y visualización por consola de la lista de espera con datos ordenados y desordenados.
*   **Benchmarking:** Medición estricta de la duración del procesamiento y consumo de memoria.

### Módulo 2 — Expedientes y Búsquedas
*   **Filtros Clínicos:** Búsquedas por cédula exacta, nombre (parcial), rango de fechas y gravedad.
*   **Análisis Algorítmico:** Cada filtro implementa **Búsqueda Lineal y Búsqueda Binaria** para contrastar su eficiencia computacional en tiempo y memoria.

### Módulo 3 — Árbol de Diagnósticos
*   **Estructura Jerárquica:** Organización taxonómica mediante un **Árbol N-ario** (*Área médica → Especialidad → Diagnóstico específico*).
*   **Operaciones:** Búsqueda por nombre o código, filtrado por especialidad y navegación.
*   **Recorridos:** Implementación de los tres recorridos clásicos (Preorden, Inorden y Postorden) sobre la estructura N-aria con métricas de rendimiento.

### Módulo 4 — Laboratorio de Rendimiento
*   **Experimentos de Ordenamiento:** Interfaz de consola para ordenar datos reales (pacientes/consultas) variando el tamaño del lote.
*   **Algoritmos en Confrontación:** *Bubble Sort, Selection Sort, Insertion Sort, Quick Sort y Merge Sort*.
*   **Gráficas en Consola:** Renderizado en tiempo real de gráficas de barras (tiempo de ejecución) y curvas de crecimiento (consumo de memoria).
*   **Confrontación de Búsqueda:** Comparación directa de Búsqueda Lineal vs. Búsqueda Binaria sobre los datos ordenados.

---

## Tecnologías y Requisitos
*   **Lenguaje:** Python 3.x
*   **Librerías/Visualización:** Gráficas nativas por consola.
