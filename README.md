

# NLQ con AWS

Esta solución contiene una demostración de IA Generativa con el fin usar de Natural Language Query (NLQ) para
hacer preguntas a una base de datos PostgreSQL (AWS RDS).


### Configuración local
Para configurar el proyecto de forma local se necesita tener instalado `docker` y `make`.

1. Clonar el repositorio `git clone git@github.com:victoraguilarc/nlq-on-aws.git`
2. Copiar las variables de entorno del archivo `.env.example` a un nuevo archivo `.env` y completar las variables con sus valores correspondientes
3. Ejecutar el comando `make build` para construir las imagenes docker del proyecto
4. Ejecutar el comando `make up` para correr el proyecto

 

### Despliegue en producción
... En desarrollo ...


## Referencias

- [Guia para consultas con lenguaje natural AWS](https://github.com/aws-solutions-library-samples/guidance-for-natural-language-queries-of-relational-databases-on-aws)
- [Vanna + Chainlit](https://github.com/vanna-ai/vanna-chainlit)
- [Vanna + flask](https://github.com/vanna-ai/vanna-flask)