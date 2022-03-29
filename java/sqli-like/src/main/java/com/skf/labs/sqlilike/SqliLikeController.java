package com.skf.labs.sqlilike;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.beans.factory.annotation.Autowired;


@Controller
public class SqliLikeController {
    @Autowired
    private SqliLikeModel sqliModel;

    @GetMapping("/home/{username}")
    public String home(@PathVariable String username, Model model) {
        List<User> users = sqliModel.getUser(username);
        model.addAttribute("user", users.get(0));
        return "index";
    }
    
}
