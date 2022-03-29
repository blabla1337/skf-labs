package com.skf.labs.idor;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class IdorApplication {

	public static void main(String[] args) {
		IdorModel.init();
		SpringApplication.run(IdorApplication.class, args);
	}

}
