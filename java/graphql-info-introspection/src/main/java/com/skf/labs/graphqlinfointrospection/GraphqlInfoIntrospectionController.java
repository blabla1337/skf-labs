package com.skf.labs.graphqlinfointrospection;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class GraphqlInfoIntrospectionController {
    
    @GetMapping("/")
    public String home(){
        return "index";
    }
}
