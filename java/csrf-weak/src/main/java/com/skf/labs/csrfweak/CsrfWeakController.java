package com.skf.labs.csrfweak;
import java.time.LocalDateTime;
import java.util.Base64;
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
public class CsrfWeakController {

   @Autowired
   private CsrfWeakModel csrfModel;

    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request) {
        List<User> users = csrfModel.getUser(username);
        if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
            request.getSession().setAttribute("loggedin",true);
            request.getSession().setAttribute("username",username);
            request.getSession().setAttribute("userId",users.get(0).getUserId());

            List<Prefs> pref = csrfModel.getColor(users.get(0).getUserId());
         

            model.addAttribute("csrfToken",newCsrfToken(request));
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
	public String update(@RequestParam(name="color", required=false) String color,@RequestParam(name="csrf_token", required=false) String csrfToken, Model model,HttpSession session,HttpServletRequest request) {
        if(null !=session.getAttribute("loggedin")){
            if(request.getMethod().equals("POST") ){
                if(csrfToken.equals(request.getSession().getAttribute("csrfToken"))){
                    csrfModel.updateColor((int)session.getAttribute("userId"), color);
                 }else{
                    model.addAttribute("content", "CSRF Token was not correct");
                 }
            }

            List<Prefs> pref = csrfModel.getColor((int)session.getAttribute("userId"));
            model.addAttribute("color", pref.get(0).getColor());
            model.addAttribute("csrfToken",newCsrfToken(request));
            return "loggedin";
        }
        return "index";
      } 

      public String newCsrfToken(HttpServletRequest request){
        String csrfToken =  request.getSession().getAttribute("username") + String.valueOf(LocalDateTime.now().getHour()) +":"+ String.valueOf(LocalDateTime.now().getMinute());
        csrfToken = Base64.getEncoder().encodeToString(csrfToken.getBytes());
        request.getSession().setAttribute("csrfToken",csrfToken);
        return csrfToken;
      }
     
}
