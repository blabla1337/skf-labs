package com.skf.labs.clickjacking;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;



@Controller
public class ClickjackingController {

    @GetMapping("/")
    public String home(){
        return "index";
    }
    
}
