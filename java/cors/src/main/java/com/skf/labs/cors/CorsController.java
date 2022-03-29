package com.skf.labs.cors;
import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@Controller
public class CorsController {

   @Autowired
   private CorsModel corsModel;

    
    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request) {
        List<User> users = corsModel.getUser(username);
        if(users.size() > 0 && (users.get(0).getPassword().equals(password))){
            request.getSession().setAttribute("loggedin",true);
            request.getSession().setAttribute("username",username);
            request.getSession().setAttribute("userId",users.get(0).getUserId());
            return "redirect:/confidential";

        }
        return "index";
      }

      @CrossOrigin(origins = "*")
      @RequestMapping(
        value = "/confidential",
        method = {
            RequestMethod.GET,
            RequestMethod.POST
        }
    )
	public String confidential( Model model,HttpSession session,HttpServletRequest request,HttpServletResponse response) {
        /**if(null !=request.getSession().getAttribute("loggedin")){
            response.addHeader("Access-Control-Allow-Credentials","true");
            return "loggedin";
        }
        return "index";
        **/
        return "loggedin";
      } 
}
