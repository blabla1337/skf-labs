package com.skf.labs.graphqldosresourceexhaustion;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class GraphqlDosResourceExhaustionController {
    
    @GetMapping("/")
    public String home(){
        return "index";
    }
}
