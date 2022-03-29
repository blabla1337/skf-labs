package com.skf.labs.csrf;
import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

@Controller
public class CsrfController {

   @Autowired
   private CsrfModel csrfModel;

    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request) {
        List<User> users = csrfModel.getUser(username);
        if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
            request.getSession().setAttribute("loggedin",true);
            request.getSession().setAttribute("username",username);
            request.getSession().setAttribute("userId",users.get(0).getUserId());

            List<Prefs> pref = csrfModel.getColor(users.get(0).getUserId());

            model.addAttribute("color", pref.get(0).getColor());

            return "loggedin";

        }
        return "index";
      }

    @RequestMapping(
        value = "/update",
        method = {
            RequestMethod.GET,
            RequestMethod.POST
        }
    )
	public String update(@RequestParam(name="color", required=false) String color, Model model,HttpSession session,HttpServletRequest request) {
        if(null !=session.getAttribute("loggedin")){

            if(request.getMethod().equals("POST")){
                csrfModel.updateColor((int)session.getAttribute("userId"), color);
            }

            List<Prefs> pref = csrfModel.getColor((int)session.getAttribute("userId"));
            model.addAttribute("color", pref.get(0).getColor());
            return "loggedin";
        }
        return "index";
      } 
     
}
