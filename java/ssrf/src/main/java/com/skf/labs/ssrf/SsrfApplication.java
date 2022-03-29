package com.skf.labs.ssrf;


import java.io.IOException;

import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

@SpringBootApplication
@PropertySource("classpath:application.properties")
public class SsrfApplication {

	public static void main(String[] args) throws IOException, InterruptedException {
		SpringApplication.run(SsrfApplication.class, args);
	}

	@Bean
    ApplicationRunner applicationRunner(Environment environment) {
        return args -> {
            SsrfModel.init(environment.getProperty("init.command"));
        };
    }
}
