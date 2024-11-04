# Usar a imagem do OpenJDK como base
FROM openjdk:17-jdk-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo gradlew e os diretórios necessários
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .
COPY src src

# Conceder permissão de execução ao script gradlew
RUN chmod +x gradlew

# Construir o aplicativo
RUN ./gradlew build --no-daemon

# Expor a porta que o aplicativo irá rodar
EXPOSE 8080

# Comando para executar o aplicativo
CMD ["java", "-jar", "build/libs/helloworld-0.0.1-SNAPSHOT.jar"]
