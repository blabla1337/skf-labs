package com.skf.labs.parameterbinding;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Cookie;

@Controller
public class ParameterBindingController {

    @Autowired
    private ParameterBindingModel authModel;

    @RequestMapping(value = "/login", method = {
            RequestMethod.GET,
            RequestMethod.POST
    })
    public String login(@RequestParam(name = "username", required = false) String username,
            @RequestParam(name = "password", required = false) String password, Model model,
            HttpServletRequest request, HttpServletResponse response) {
        if (request.getMethod().equals("POST")) {
            List<User> users = authModel.getUser(username);
            if (users.size() > 0 && (users.get(0).getPassword().equals(password))) {
                request.getSession().setAttribute("loggedin", true);
                request.getSession().setAttribute("username", username);

                model.addAttribute("username", username);
                model.addAttribute("isAdmin", users.get(0).getIsAdmin());

                return "loggedin";
            }
        }
        return "index";
    }

    @PostMapping("/create")
    public String createUser(User user, Model model) {
        authModel.createUser(user);
        model.addAttribute("content", "Your user has been created");
        return "index";
    }

    @GetMapping("/register")
    public String register(Model model, HttpServletRequest request) {
        model.addAttribute("renderLogout", isLoggedIn(request));
        return "register";
    }

    public boolean isLoggedIn(HttpServletRequest request) {
        if (null != request.getSession().getAttribute("loggedin")) {
            return true;
        } else {
            return false;
        }
    }

    @GetMapping("/logout")
    public String logout(Model model, HttpServletRequest request) {
        Cookie cookies[] = request.getCookies();
        for (Cookie c : cookies) {
            c.setValue(null);
        }

        request.getSession().invalidate();
        model.addAttribute("content", "You successfully logged out");
        return "index";
    }
}
