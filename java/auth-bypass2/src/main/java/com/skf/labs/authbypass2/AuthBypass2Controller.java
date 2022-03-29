package com.skf.labs.authbypass2;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.apache.commons.codec.digest.DigestUtils;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.servlet.http.Cookie;

@Controller
public class AuthBypass2Controller {

    @Autowired
    private AuthBypass2Model authModel;

    @RequestMapping(value = "/login", method = {
            RequestMethod.GET,
            RequestMethod.POST
    })
    public String login(@RequestParam(name = "username", required = false) String username,
            @RequestParam(name = "password", required = false) String password,
            @CookieValue(name = "userId", required = false) String userIdCookie, Model model,
            HttpServletRequest request, HttpServletResponse response) {
        if (request.getMethod().equals("POST")) {
            List<User> users = authModel.getUser(username);
            if (users.size() > 0 && (users.get(0).getPassword().equals(password))) {
                request.getSession().setAttribute("loggedin", true);
                request.getSession().setAttribute("username", username);

                response.addCookie(new Cookie("sessionId", DigestUtils.sha1Hex(username + "SKFowaspLabs")));
                model.addAttribute("username", username);
                model.addAttribute("content", "Find the way to login as an admin!");

                return "loggedin";
            }
        }
        return "index";
    }

    @PostMapping("/create")
    public String createUser(@RequestParam(name = "username", required = true) String username,
            @RequestParam(name = "password", required = true) String password, Model model) {

        List<User> users = authModel.getUser(username.toLowerCase());
        if (!users.isEmpty()) {
            if (!username.toLowerCase().equals("admin")) {
                authModel.updatePassword(password, username);
                model.addAttribute("content", "Your password has been updated");
            } else {
                model.addAttribute("content", "Nice try! ;-)");
            }
            return "index";

        } else {
            User u = new User(username, password, DigestUtils.sha1Hex(username + "SKFowaspLabs"));
            authModel.createUser(u);
            model.addAttribute("content", "Your user has been created");
            return "index";
        }

    }

    @GetMapping("/loggedin")
    public String loggedin(@CookieValue(name = "sessionId", required = false) String sessionId, Model model,
            HttpServletRequest request) {
        if (isLoggedIn(request)) {
            List<User> users = authModel.getHash(sessionId);
            if (users.get(0).getUsername().toLowerCase().equals("admin")) {
                model.addAttribute("content", "Congratulations!");
            } else {
                model.addAttribute("content", "Find the way to login as an admin!");
            }
            model.addAttribute("username", users.get(0).getUsername().toLowerCase());
            return "loggedin";

        }
        model.addAttribute("content", "You have to login first");
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

    @GetMapping("/about")
    public String about() {
        return "about";
    }
}
