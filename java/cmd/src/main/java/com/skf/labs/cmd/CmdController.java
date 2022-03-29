package com.skf.labs.cmd;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class CmdController {
    
    @PostMapping("/home")
	public String login(@RequestParam(name="size", required=true) String sizeImg) throws IOException, InterruptedException{
        Process pb = new ProcessBuilder("/bin/sh","-c","convert repo/bones.png -resize "+sizeImg+"% repo/bones.png").redirectErrorStream(true).start();
        return "index";
      }
}
