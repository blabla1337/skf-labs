package com.skf.labs.jwtnull;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class JwtNullApplication {

	public static void main(String[] args) {
		JwtModel.init();
		SpringApplication.run(JwtNullApplication.class, args);
	}

}
