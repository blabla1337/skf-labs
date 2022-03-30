package com.skf.labs.ldapinjection;

import java.io.IOException;


public class LdapInjectionModel {
   
    public static void init(String startUpCmd) throws IOException, InterruptedException{
		ProcessBuilder pb = new ProcessBuilder("/bin/sh",startUpCmd);
		pb.start();
    }
    
}
