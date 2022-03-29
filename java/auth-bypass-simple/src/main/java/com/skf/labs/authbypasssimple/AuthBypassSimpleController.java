package com.skf.labs.authbypasssimple;
import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.servlet.http.Cookie;

@Controller
public class AuthBypassSimpleController {

   @Autowired
   private AuthBypassSimpleModel authModel;

   @RequestMapping(
    value = "/login",
    method = {
        RequestMethod.GET,
        RequestMethod.POST
    }
)
	public String login(@RequestParam(name="username", required=false) String username,@RequestParam(name="password", required=false) String password, @CookieValue(name = "userId", required = false) String userIdCookie,Model model, HttpServletRequest request,HttpServletResponse response) {
        if(request.getMethod().equals("POST")){
            List<User> users = authModel.getUser(username);
            if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
                request.getSession().setAttribute("loggedin",true);
                request.getSession().setAttribute("username",username);
                request.getSession().setAttribute("userId",users.get(0).getUserId());

                List<Prefs> pref = authModel.getApiKey(users.get(0).getUserId());

                response.addCookie(new Cookie("userId",String.valueOf(users.get(0).getUserId())));
                model.addAttribute("apikey", pref.get(0).getAPIkey());
                return "loggedin";
            }
        }else{
           if(null != userIdCookie){
            List<Prefs> pref = authModel.getApiKey(Integer.parseInt(userIdCookie));
            model.addAttribute("apikey", pref.get(0).getAPIkey());
            return "loggedin";
           }

        }
        return "index";
      }
}
