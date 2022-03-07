FROM adoptopenjdk/openjdk8
VOLUME ["/tmp", "/logs"]
EXPOSE 8848
ADD /target/decsion-engine-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]