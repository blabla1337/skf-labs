package com.skf.labs.credentialsguessing1;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;


@Controller
public class CredentialsGuessingController {
    @Autowired
    private CredentialsGuessingModel credentialsGuessingModel;

    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request) {
        List<User> users = credentialsGuessingModel.getUser(username);
        if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
            request.getSession().setAttribute("loggedin",true);
            request.getSession().setAttribute("username",username);
            request.getSession().setAttribute("userId",users.get(0).getUserId());


            return "loggedin";

        }
        return "index";
      }

}
