package com.skf.labs.desyaml;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.yaml.snakeyaml.Yaml;
import java.util.Base64;

@Controller
public class DesYamlController {

    @GetMapping("/config/{input}")
    public String input(@PathVariable String input, Model model) {
        byte[] decodedInputBytes = Base64.getDecoder().decode(input);
        String decodedString = new String(decodedInputBytes);
        Yaml yaml = new Yaml();
        Object obj = yaml.load(decodedString);     
        model.addAttribute("content",obj.toString());
        return "index.html";
      }

    
}
