# Definición de producto · Envaplast Cobranzas AI

## Scoring v1.0 y efecto de los filtros

El puntaje se calcula primero sobre la cartera abierta completa. Saldo vencido y concentración
se normalizan de forma relativa contra la composición del conjunto; por eso el puntaje de un
cliente puede cambiar cuando cambia la cartera, aunque sus propios datos permanezcan iguales.
Los filtros de prioridad, estado y responsable se aplican después del cálculo: acotan la cola
visible, pero no recalculan ni alteran el orden relativo de los casos que permanecen visibles.

Los saldos nulos o negativos se excluyen de la cola. Un límite de crédito igual a cero aporta
cero al factor de utilización y no provoca divisiones inválidas. Los umbrales de clasificación
son inclusivos: 45 puntos inicia prioridad Alta y 70 puntos inicia prioridad Crítica.

## Propósito

Envaplast Cobranzas AI ayuda a una persona responsable de cobranzas en una PyME a decidir **qué cuenta gestionar primero, por qué y cuál es el siguiente paso sugerido**.

El producto toma la cartera abierta de Envaplast Analytics como contexto de negocio y la convierte en una cola de trabajo explicable. No reemplaza el criterio profesional ni envía comunicaciones automáticamente.

## Usuario principal

Responsable administrativo, financiero o de cobranzas que:

- gestiona una cartera distribuida entre planillas o sistemas;
- necesita priorizar casos con tiempo limitado;
- debe justificar por qué una cuenta requiere atención;
- conserva la decisión final y el vínculo con el cliente.

## Problema

Ordenar únicamente por saldo, mora o fecha de vencimiento produce prioridades parciales. La gestión necesita combinar exposición, antigüedad, presión sobre el límite de crédito y concentración para enfocar primero los casos de mayor riesgo e impacto.

## Flujo del MVP

1. **Entender:** resume cartera abierta, saldo vencido, casos críticos y cobertura del top 10.
2. **Priorizar:** agrupa facturas por cliente y calcula un puntaje de 0 a 100.
3. **Explicar:** muestra las señales que sostienen la posición de cada cuenta.
4. **Recomendar:** propone una próxima acción según puntaje y mora.
5. **Preparar:** genera un borrador editable de contacto.
6. **Revisar:** una persona decide, modifica y ejecuta la comunicación fuera del sistema.

## Scoring explicable

El puntaje es una regla determinística y auditable. **No es un modelo predictivo, una probabilidad de cobro ni un sistema entrenado con datos históricos.**

| Factor | Peso máximo | Cálculo actual |
|---|---:|---|
| Saldo vencido | 35 | Saldo vencido del cliente respecto del mayor saldo vencido de la cartera analizada |
| Mora | 25 | Días máximos de mora, con saturación a 90 días |
| Uso del crédito | 20 | Saldo abierto sobre límite de crédito, con saturación a 150% |
| Concentración | 20 | Participación del cliente respecto de la mayor participación de la cartera analizada |

```text
puntaje = saldo vencido (0–35)
        + mora (0–25)
        + uso del crédito (0–20)
        + concentración (0–20)
```

### Niveles de prioridad

- **Crítica:** 70 puntos o más.
- **Alta:** entre 45 y 69,9 puntos.
- **Seguimiento:** menos de 45 puntos.

### Interpretación correcta

Los componentes de saldo vencido y concentración son relativos al conjunto analizado. Por eso el puntaje sirve para **ordenar la cartera actual**, pero no para comparar sin recalibración carteras de empresas, períodos o filtros muy diferentes.

## Ejemplo de decisión

Un cliente puede quedar primero cuando combina:

- saldo vencido elevado;
- mora máxima superior a 90 días;
- uso del límite de crédito igual o mayor al 100%;
- participación material en la cartera total.

El producto muestra esas señales, propone contactarlo hoy y prepara un borrador. La persona responsable puede considerar acuerdos comerciales, reclamos, documentación pendiente u otra información no incluida antes de actuar.

## Human-in-the-loop

El MVP aplica cuatro límites deliberados:

- no envía correos, mensajes ni notificaciones;
- no bloquea cuentas ni modifica límites de crédito;
- no promete fechas ni condiciones en nombre del cliente;
- no oculta los factores del ranking.

El borrador es editable y descargable. La decisión final permanece bajo revisión humana.

## Alcance actual

### Entregado

- cola de cobranzas agrupada por cliente;
- scoring explicable y prioridades;
- KPIs de impacto;
- explicación de factores;
- acción recomendada;
- borrador editable y descargable;
- gestión persistente por cliente con estado, responsable y notas;
- compromiso de pago;
- historial de eventos;
- exclusión de casos resueltos de la cola activa;
- datos sintéticos;
- pruebas unitarias específicas del ranking y del mensaje.

### Necesario para v1.0

- captura propia de la pantalla Cobranzas AI;
- validaciones adicionales para estabilidad del ranking;
- medición del tiempo ahorrado y cobertura gestionada;
- documentación de cambios de pesos y umbrales.

### Fuera de alcance por ahora

- envío automático de comunicaciones;
- predicción de incobrabilidad;
- entrenamiento de modelos con datos reales;
- decisiones automáticas sobre crédito;
- integración productiva con ERP, correo o mensajería.

## Criterios de éxito para portfolio

La versión Portfolio Ready deberá demostrar:

1. Un flujo completo desde cartera abierta hasta acción revisada.
2. Trazabilidad entre puntaje, factores y recomendación.
3. Pruebas de reglas y casos límite.
4. Una captura y narrativa propias, sin depender del dashboard general.
5. Diferenciación explícita entre reglas determinísticas, automatización e IA generativa.
6. Release pública `v1.0.0` con demo verificada.
