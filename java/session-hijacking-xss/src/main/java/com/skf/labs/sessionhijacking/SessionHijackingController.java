package com.skf.labs.sessionhijacking;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;

@Controller
public class SessionHijackingController {
    @Autowired
    private SessionHijackingModel SessionHijackingModel;

    @GetMapping("/login")
    public String message(Model model, HttpServletRequest request) {
        if (request.getSession().getAttribute("loggedin") != null) {
            return "loggedin";
        }
        return "index";
    }

    @PostMapping("/login")
    public String login(@RequestParam(name = "username", required = true) String username,
            @RequestParam(name = "password", required = true) String password, Model model,
            HttpServletRequest request) {
        List<User> users = SessionHijackingModel.getUser(username);
        if (users.size() > 0 && (users.get(0).getPassword().equals(password))) {
            request.getSession().setAttribute("loggedin", true);
            request.getSession().setAttribute("username", username);
            request.getSession().setAttribute("userId", users.get(0).getUserId());

            return "loggedin";

        }
        return "index";
    }

    @PostMapping("/message")
    public String message(@RequestParam(name = "message", required = true) String message,
            Model model, HttpServletRequest request) {
        if (request.getSession().getAttribute("loggedin") != null) {
            SessionHijackingModel.updateMessage((int) request.getSession().getAttribute("userId"), message);
            List<Prefs> pref = SessionHijackingModel
                    .getMessage(Integer.parseInt(request.getSession().getAttribute("userId").toString()));
            model.addAttribute("message", pref.get(0).getAPIkey());
            return "loggedin";
        }
        return "index";
    }

}
