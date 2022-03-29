package com.skf.labs.desjava;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.CookieValue;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;
import java.util.Base64;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;


@Controller
public class DesJavaController {

    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="role", required=true) String role,Model model,HttpServletResponse response) {
        User user = new User(username, role);
        ByteArrayOutputStream baos = new ByteArrayOutputStream(512);
        String sessionCookie = "";
        try{
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(user);
            sessionCookie = Base64.getEncoder().encodeToString(baos.toByteArray());
        }catch(Exception e){
            e.printStackTrace();
        }
        response.addCookie(new Cookie("session",sessionCookie));
        return "redirect:/loggedin";
      }

      @GetMapping("/loggedin")
      public String loggedIn( @CookieValue(name = "session", required = false) String sessionCookie,Model model){

        if(null != sessionCookie){
            try{
                ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(Base64.getDecoder().decode(sessionCookie)));
                Object obj = ois.readObject();
                if((obj instanceof User)){
                    User user = (User) obj;
                    model.addAttribute("user", user.getUsername());
                    model.addAttribute("role", user.getRole());
                    return "loggedin";
                }else{
                    return "index";
                }
            }catch(Exception e){
                e.printStackTrace();
                return "index";
            }
        }
        return "index";
      }
}
