package com.skf.labs.authbypass3;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.ui.Model;





@Controller
public class AuthBypass3Controller{

    @PostMapping("/home")
	public String home(@RequestParam(name="pois_url", required=true) String url,Model model) {
        model.addAttribute("content", url);
        return "index";
    }

    @PostMapping("/signup")
	public String signup(@RequestParam(name="username", required=true) String username,Model model) {
        model.addAttribute("content", username);
        return "user_created_right";
    }

    @GetMapping("/users/{user_id}")
    public String user(@PathVariable String user_id, Model model) {
        if(user_id.equals("user01")){
            model.addAttribute("username","bob");
            model.addAttribute("password","abcd1234");
            model.addAttribute("content","Your secret message: [STILL NOT SET]");
            return "useraccount";
        }else if(user_id.equals("user02")){
            model.addAttribute("username","admin");
            model.addAttribute("password","rootadmin");
            model.addAttribute("content","I am the admin of this website.");
            return "useraccount";
        }else{
            model.addAttribute("username","You need to set your user account");
            model.addAttribute("password","You need to set your password");
            model.addAttribute("content","You need to set your data");
            return "useraccount_empty";
        }
    }

    
}
