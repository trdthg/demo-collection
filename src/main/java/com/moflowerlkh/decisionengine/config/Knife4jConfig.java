//改配置文件和Swagger配置文件一致，只是添加了两个注解
package com.moflowerlkh.decisionengine.config;

import com.github.xiaoymin.knife4j.spring.annotations.EnableKnife4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.ParameterBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.schema.ModelRef;
import springfox.documentation.service.Parameter;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import java.util.ArrayList;
import java.util.List;

@Configuration
@EnableKnife4j
@EnableSwagger2
@ConditionalOnProperty(name = "active", havingValue = "false")
public class Knife4jConfig {
    @Bean
    public Docket createRestApi(Environment environment) {
        // Swagger 2 使用的是：DocumentationType.SWAGGER_2
        // Swagger 3 使用的是：DocumentationType.OAS_30

        ParameterBuilder ticketPar = new ParameterBuilder();
        List<Parameter> pars = new ArrayList<>();
        ticketPar.name("Authorization").description("token")
            .modelRef(new ModelRef("string")).parameterType("header")
            .required(false).build(); //header中的ticket参数非必填，传空也可以
        pars.add(ticketPar.build());    //根据每个方法名也知道当前方法在设置什么参数

        return new Docket(DocumentationType.SWAGGER_2)
            .apiInfo(new ApiInfoBuilder()
                .title("decision-engine RESTful APIs")
                .description("决策引擎Restful API")
                .version("1.0")
                .build())
            .groupName("2.X版本")
            .select()
            //.apis(RequestHandlerSelectors.basePackage("com.moflowerlkh.decisionengine.controller"))
            .paths(PathSelectors.any())
            .build()
            .globalOperationParameters(pars);
    }

}
