package com.skf.labs.cmdblind;

import java.io.IOException;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class CmdBlindController {

  @PostMapping("/home")
  public String login(@RequestParam(name = "text") String text)
      throws IOException, InterruptedException {
    new ProcessBuilder("/bin/sh", "-c", "echo " + text + " >> welcome")
        .redirectErrorStream(true).start();
    return "index";
  }
}
