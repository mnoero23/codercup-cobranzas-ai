# Caso de negocio · Cobranzas AI

## Situación

Una PyME industrial administra una cartera distribuida entre facturas, planillas y registros
de contacto. El equipo dispone de pocas horas para gestionar decenas de clientes y ordenar sólo
por saldo o mora deja afuera parte del riesgo comercial.

## Decisión que mejora

La persona responsable necesita responder tres preguntas al comenzar la jornada:

1. ¿Qué cliente requiere atención primero?
2. ¿Qué factores justifican esa prioridad?
3. ¿Cuál es el próximo paso y quién debe realizarlo?

## Solución

Cobranzas AI agrupa la cartera por cliente y calcula un puntaje auditable de 0 a 100. Combina
saldo vencido, mora, uso del límite de crédito y concentración. Luego propone una acción,
prepara un borrador editable y permite registrar responsable, estado, notas y compromisos.

No predice incobrabilidad ni contacta automáticamente. La decisión permanece en manos de una
persona y cada actualización queda registrada en el historial.

## Caso demostrativo

La cartera sintética incluye tres situaciones preparadas:

| Estado | Situación | Decisión visible |
|---|---|---|
| Contactado | Documentación reenviada y fecha de pago solicitada | Mantener seguimiento asignado |
| Comprometido | Pago parcial confirmado para la semana siguiente | Controlar fecha e importe prometidos |
| Resuelto | Pago acreditado y conciliado | Retirar de la cola activa y conservar historial |

El ranking también indica cuántos clientes del top 10 no aparecerían si se ordenara únicamente
por saldo, haciendo visible el aporte del enfoque multivariable.

## Impacto esperado

El producto busca reducir el tiempo de preparación diaria, aumentar la cobertura monetaria de
las gestiones y evitar que compromisos o antecedentes queden dispersos. Al trabajar con datos
sintéticos, estos beneficios se presentan como impacto potencial y no como resultados reales.

Una implementación productiva mediría:

- tiempo hasta la primera gestión;
- porcentaje de cartera gestionada;
- cumplimiento de compromisos;
- recupero posterior al contacto;
- comparación contra una priorización sólo por saldo o mora.

## Alcance y límites

- Datos completamente sintéticos y reproducibles.
- Scoring determinístico, no machine learning.
- Sin envío automático de correos o mensajes.
- Sin decisiones automáticas sobre crédito.
- Sin integración productiva con ERP.
- Revisión humana obligatoria antes de actuar.
