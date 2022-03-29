package com.skf.labs.cmd2;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class Cmd2Controller {

  @GetMapping("/compress")
  public String compress(@RequestParam(name = "log_type") String log_type, Model model)
      throws IOException, InterruptedException {
    // create process to zip the log file
    Process pb = new ProcessBuilder("/bin/sh", "-c",
        "zip log.zip " + log_type + "_log.txt")
        .redirectErrorStream(true)
        .start();
    // read the output of the process
    BufferedReader br = new BufferedReader(new InputStreamReader(pb.getInputStream()));
    /* System.out.println(br.readLine()); */
    model.addAttribute("os_result", br.readLine());
    return "index";
  }

  @GetMapping("/viewer")
  public String viewer(@RequestParam(name = "lines") String lines, Model model)
      throws IOException, InterruptedException {
    BufferedReader br = new BufferedReader(new FileReader(lines + "_log.txt"));
    String print_result = "<div style='border: thin solid black;padding: 10px;display: inline-block;'><b> " + lines
        + "_log.txt</b></div><br/><br/>";
    for (int i = 0; i < 15; i++) {
      print_result += br.readLine();
      print_result += "<br/>";
    }
    model.addAttribute("print_result", print_result);
    return "index";
  }

}
