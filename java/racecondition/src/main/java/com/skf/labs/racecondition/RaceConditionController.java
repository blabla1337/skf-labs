package com.skf.labs.racecondition;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class RaceConditionController {

  @GetMapping("/")
  public String index(@RequestParam Map<String, String> params, Model model) {
    String action = params.getOrDefault("action", "run");
    String hello = "";
    if (action.equals("validate")) {
      String person = params.getOrDefault("person", "Default User");
      String valid = bootValidate(person);
      if (valid == "") {
        bootClean();
      }
    } else if (action.equals("reset")) {
      bootClean();
      bootReset();
      bootRun();
    } else {
      bootRun();
      try (FileReader fr = new FileReader("hello.txt")) {
        BufferedReader br = new BufferedReader(fr);
        hello = br.readLine();
        model.addAttribute("hello", hello);
      } catch (IOException e) {
        hello = "Important hello file is missing, please reset.";
        bootClean();
        bootReset();
        bootRun();
      }
    }
    model.addAttribute("action", action);
    model.addAttribute("hello", hello);
    return "index";
  }

  public String bootValidate(String person) {
    try (FileWriter writer = new FileWriter("hello.sh", false)) {
      writer.write("echo \"" + person + "\" > hello.txt");
      writer.close();
      java.util.Date date = new java.util.Date();
      new ProcessBuilder("/bin/bash", "-c", "echo 'hello.sh updated -- " + date + "' > log.txt").start();
      new ProcessBuilder("/bin/bash", "-c", "echo 'hello.sh cleaned -- " + date + "' >> log.txt").start();
      Process p3 = new ProcessBuilder("/bin/bash", "-c", "sed -n '/^echo \"[A-Za-z0-9 ]*\" > hello.txt$/p' hello.sh")
          .start();
      BufferedReader reader = new BufferedReader(new java.io.InputStreamReader(p3.getInputStream()));
      String valid = reader.readLine();
      System.out.println(valid);
      return valid == null ? "" : valid;
    } catch (Exception e) {
      e.printStackTrace();
    }
    return "";
  }

  private void bootClean() {
    try {
      new ProcessBuilder("/bin/bash", "-c", "rm hello.*").start().waitFor();
    } catch (IOException e) {
      e.printStackTrace();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }

  private void bootRun() {
    try {
      new ProcessBuilder("/bin/bash", "-c", "bash hello.sh").start().waitFor();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private void bootReset() {
    try {
      new ProcessBuilder("/bin/bash", "-c", "echo 'echo \"Default User\" > hello.txt' > hello.sh").start().waitFor();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
