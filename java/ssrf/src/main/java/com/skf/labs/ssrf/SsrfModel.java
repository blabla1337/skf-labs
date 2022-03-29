package com.skf.labs.ssrf;

import java.io.IOException;


public class SsrfModel {
   
    public static void init(String startUpCmd) throws IOException, InterruptedException{
		ProcessBuilder pb = new ProcessBuilder("/bin/sh",startUpCmd);
		pb.start();
    }
    
}
