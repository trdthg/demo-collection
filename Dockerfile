FROM adoptopenjdk/openjdk8
VOLUME ["/tmp", "/logs"]
EXPOSE 8848
ADD /target/decsion-engine-0.1.5.jar app.jar
# ADD ./agent agent
ENTRYPOINT ["java", "-jar", "app.jar"]
# CMD java -javaagent:agent/skywalking-agent.jar -Dskywalking.agent.service_name=xxx -Dskywalking.collector.backend_service=oap:11800 -jar app.jar