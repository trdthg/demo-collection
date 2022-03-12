FROM adoptopenjdk/openjdk8
VOLUME ["/tmp", "/logs"]
EXPOSE 8848
ADD /target/decsion-engine-0.1.5.jar app.jar
ADD ./agent agent
# ADD ./skywalking-agent.jar skywalking-agent.jar
# ENTRYPOINT ["java", "-jar", "app.jar"]
# ENTRYPOINT ["java", "-javaagent:agent/skywalking-agent.jar", "-Dskywalking.agent.service_name=xxx", "-Dskywalking.collector.backend_service=192.168.31.226:11800", "-jar", "app.jar"]
CMD java -javaagent:agent/skywalking-agent.jar -Dskywalking.agent.service_name=xxx -Dskywalking.collector.backend_service=oap:11800 -jar app.jar
# ENTRYPOINT ["java", "-javaagent:agent/skywalking-agent.jar", "-Dskywalking.agent.service_name=xxx", "-Dskywalking.collector.backend_service=oap:11800", "-jar", "app.jar"]
# ENTRYPOINT ["java", "-javaagent:skywalking-agent.jar", "-Dskywalking.agent.service_name=xxx", "-Dskywalking.collector.backend_service=oap:11800", "-jar", "app.jar"]
# java -javaagent:<skywalking-agent-path>
# -Dskywalking.agent.service_name=<ServiceName>
# -Dskywalking.collector.backend_service=<backend-service-addresses>
# -jar yourApp.jar

# "-javaagent:/skywalking.jar",