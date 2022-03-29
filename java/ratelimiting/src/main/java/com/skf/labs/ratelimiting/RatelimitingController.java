package com.skf.labs.ratelimiting;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpServletRequest;

@Controller
public class RatelimitingController {

    @PostMapping("/login")
    public String login(@RequestParam(name = "username", required = true) String username,
            @RequestParam(name = "password", required = true) String password, Model model,
            HttpServletRequest request) {

        if (!username.equals("devteam") || !password.equals("manchesterunited")) {
            model.addAttribute("error", "Invalid username or password");
            return "index";
        } else {
            return "pwned";
        }
    }

}
