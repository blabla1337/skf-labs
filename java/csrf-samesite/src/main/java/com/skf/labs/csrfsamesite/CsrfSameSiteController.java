package com.skf.labs.csrfsamesite;
import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import javax.servlet.http.HttpSession;

@Controller
public class CsrfSameSiteController {

   @Autowired
   private CsrfSameSiteModel csrfModel;

    @PostMapping("/login_insecure")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request) {
        List<User> users = csrfModel.getUser(username);
        if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
            request.getSession();
            request.changeSessionId();
            request.getSession().setAttribute("loggedin",true);
            request.getSession().setAttribute("username",username);
            request.getSession().setAttribute("userId",users.get(0).getUserId());

            List<Prefs> pref = csrfModel.getColor(users.get(0).getUserId());

            model.addAttribute("color", pref.get(0).getColor());

            return "loggedin";

        }
        return "index";
      }

      @PostMapping("/login_strict")
      public String login_strict(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request, HttpServletResponse response) {
          List<User> users = csrfModel.getUser(username);
          if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
              request.getSession();
              request.changeSessionId();
              String sessionID = request.getRequestedSessionId();
              response.setHeader("Set-Cookie", "JSESSIONID="+sessionID+"; HttpOnly; SameSite=strict");
              request.getSession().setAttribute("loggedin",true);
              request.getSession().setAttribute("username",username);
              request.getSession().setAttribute("userId",users.get(0).getUserId());
              List<Prefs> pref = csrfModel.getColor(users.get(0).getUserId());
  
              model.addAttribute("color", pref.get(0).getColor());
  
              return "loggedin";
  
          }
          return "index";
        }


        @PostMapping("/login_lax")
        public String login_lax(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request,HttpServletResponse response) {
            List<User> users = csrfModel.getUser(username);
            if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
                request.getSession();
                request.changeSessionId();
                String sessionID = request.getRequestedSessionId();
                response.setHeader("Set-Cookie", "JSESSIONID="+sessionID+"; HttpOnly; SameSite=lax");
                request.getSession().setAttribute("loggedin",true);
                request.getSession().setAttribute("username",username);
                request.getSession().setAttribute("userId",users.get(0).getUserId());
    
                List<Prefs> pref = csrfModel.getColor(users.get(0).getUserId());
    
                model.addAttribute("color", pref.get(0).getColor());
    
                return "loggedin";
    
            }
            return "index";
          }

    @PostMapping("/update")
	public String updatePost(@RequestParam(name="color", required=true) String color, Model model,HttpSession session,HttpServletRequest request) {
        if(null !=session.getAttribute("loggedin")){
            csrfModel.updateColor((int)session.getAttribute("userId"), color);
            return "loggedin";
        }
        return "index";
      } 

      @GetMapping("/update")
      public String updateGet(@RequestParam(name="color", required=false) String color, Model model,HttpSession session,HttpServletRequest request) {
          if(null !=session.getAttribute("loggedin")){
  
              if(null != color){
                  csrfModel.updateColor((int)session.getAttribute("userId"), color);
              }
  
              List<Prefs> pref = csrfModel.getColor((int)session.getAttribute("userId"));
              model.addAttribute("color", pref.get(0).getColor());
              return "loggedin";
          }
          return "index";
        } 
       
     
}
