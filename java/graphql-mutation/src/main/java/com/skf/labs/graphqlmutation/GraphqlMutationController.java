package com.skf.labs.graphqlmutation;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class GraphqlMutationController {
    
    @GetMapping("/")
    public String home(){
        return "index";
    }
}
