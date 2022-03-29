package com.skf.labs.jwtsecret;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class JwtSecretApplication {

	public static void main(String[] args) {
		JwtModel.init();
		SpringApplication.run(JwtSecretApplication.class, args);
	}

}
