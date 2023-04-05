package com.skf.labs.ssti;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class SstiController {
    @GetMapping("/home/{pageId}")
    public String home(@PathVariable int pageId){
        switch(pageId){
            case 1:
            return "redirect:/error/404";
            case 2:
            return "redirect:/error/500";
            default:  
            return "redirect:/";
        }
      
    }

    @GetMapping("/error/{code}")
    public String error(@PathVariable String code){
        return "error/"+code;
    }
}
