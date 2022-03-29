package com.skf.labs.rfi;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.servlet.http.HttpServletRequest;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class RfiController {

  @GetMapping("/")
  public String index(Model model) {
    return "index";
  }

  @PostMapping("/cmd")
  public String login(@RequestParam(name = "filename", required = true) String filename, Model model)
      throws IOException, InterruptedException {
    HttpServletRequest request = ((org.springframework.web.context.request.ServletRequestAttributes) org.springframework.web.context.request.RequestContextHolder
        .getRequestAttributes())
        .getRequest();
    String url = request.getRequestURL().toString();
    if (!filename.contains("http")) {
      String host = url.substring(0, url.lastIndexOf("/"));
      filename = host + "/" + filename;
    }
    URL path = new URL(filename);
    HttpURLConnection conn = (HttpURLConnection) path.openConnection();
    BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
    String output = in.readLine();
    Process p = new ProcessBuilder("/bin/sh", "-c", output).redirectErrorStream(true).start();
    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
    model.addAttribute("result", br.readLine());
    return "index";
  }
}
