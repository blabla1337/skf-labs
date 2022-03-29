package com.skf.labs.sessionpuzzle;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.GetMapping;
import org.apache.commons.codec.digest.DigestUtils;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Cookie;

@Controller
public class SessionPuzzleController {

    @Autowired
    private SessionPuzzleModel authModel;

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
                return "dashboard";
            }
        }
        return "index";
    }

    @GetMapping("/dashboard")
    public String loggedin(Model model,
            HttpServletRequest request) {
        if (isLoggedIn(request)) {
            model.addAttribute("username", request.getSession().getAttribute("username"));
            return "dashboard";
        }
        model.addAttribute("error", "You have to login first");
        return "index";
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
        model.addAttribute("error", "You successfully logged out");
        return "index";
    }

    @GetMapping("/forgot")
    public String forgot(Model model) {
        return "forgot";
    }

    @PostMapping("/forgot")
    public String forgot(@RequestParam(name = "username", required = false) String username,
            Model model, HttpServletRequest request) {
        List<User> users = authModel.getUser(username);
        if (users.size() > 0) {
            String newPassword = DigestUtils.sha256Hex(username);
            authModel.updatePassword(username, newPassword);
            request.getSession().setAttribute("loggedin", true);
            model.addAttribute("error",
                    "If your username is registered with us,  you will receive an email with the new password");
            return "forgot";
        } else {
            model.addAttribute("error",
                    "If your username is registered with us,  you will receive an email with the new password");
            return "forgot";
        }
    }
}
