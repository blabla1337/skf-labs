package com.skf.labs.clientsiderestrictionbypass;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;

@Controller
public class ClientSideRestrictionBypassController {
    @Autowired
    private ClientSideRestrictionBypassModel ClientSideRestrictionBypassModel;

    @GetMapping("/login")
    public String message(Model model, HttpServletRequest request) {
        if (request.getSession().getAttribute("loggedin") != null) {
            // get the user's preferences
            List<Prefs> prefs = ClientSideRestrictionBypassModel
                    .getPrefs((int) request.getSession().getAttribute("userId"));
            model.addAttribute("color", prefs.get(0).getColor());
            model.addAttribute("food", prefs.get(0).getFood());
            return "loggedin";
        }
        return "index";
    }

    @PostMapping("/login")
    public String login(@RequestParam(name = "username", required = true) String username,
            @RequestParam(name = "password", required = true) String password, Model model,
            HttpServletRequest request) {
        List<User> users = ClientSideRestrictionBypassModel.getUser(username);
        if (users.size() > 0 && (users.get(0).getPassword().equals(password))) {
            request.getSession().setAttribute("loggedin", true);
            request.getSession().setAttribute("username", username);
            request.getSession().setAttribute("userId", users.get(0).getUserId());
            List<Prefs> prefs = ClientSideRestrictionBypassModel.getPrefs(users.get(0).getUserId());
            model.addAttribute("color", prefs.get(0).getColor());
            model.addAttribute("food", prefs.get(0).getFood());
            return "loggedin";
        }
        return "index";
    }

    @PostMapping("/updatecolor")
    public String updateColor(@RequestParam(name = "color", required = true) String color,
            HttpServletRequest request) {
        ClientSideRestrictionBypassModel.updateColor((int) request.getSession().getAttribute("userId"), color);
        return "redirect:/login";
    }

    @PostMapping("/updatefood")
    public String updateFood(@RequestParam(name = "food", required = true) String food,
            HttpServletRequest request) {
        ClientSideRestrictionBypassModel.updateFood((int) request.getSession().getAttribute("userId"), food);
        return "redirect:/login";
    }

}
