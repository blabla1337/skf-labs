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
  public String login(@RequestParam(name = "size", required = true) String sizeImg)
      throws IOException, InterruptedException {
    ProcessBuilder pb = new ProcessBuilder("/bin/sh", "-c",
        "convert src/main/resources/static/img/bones.png -resize " + sizeImg
            + "%  src/main/resources/static/img/bones.png");
    pb.start();
    return "index";
  }
}
