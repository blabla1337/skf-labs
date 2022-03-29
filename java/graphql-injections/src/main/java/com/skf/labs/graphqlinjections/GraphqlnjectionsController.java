package com.skf.labs.graphqlinjections;



import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.beans.factory.annotation.Autowired;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.skf.labs.graphqlinjections.entity.User;
import com.skf.labs.graphqlinjections.entity.UserInfo;
import com.skf.labs.graphqlinjections.repository.UserInfoRepository;
import com.skf.labs.graphqlinjections.repository.UserRepository;

import javax.servlet.http.Cookie;





@Controller
public class GraphqlnjectionsController {

    @Autowired 
    UserInfoRepository userInfoRepository;

    @Autowired 
    UserRepository userRepository;
   
    @GetMapping("/")
    public String home(@CookieValue(name = "X-Api-Key", required = false) String apiKey, Model model){
       UserInfo userInfo = userInfoRepository.findUserInfoByApiKey(apiKey);
       
       if(null != userInfo){
            model.addAttribute("content", userInfo.getName() +" "+ userInfo.getSurname());
            return "index";
        }else{
            return "login";
        }
    }

    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model, HttpServletRequest request,HttpServletResponse response) {
        User user = userRepository.findUserByUsernamePassword(username,password);
        
        if(null!=user){
            UserInfo userInfo  = userInfoRepository.findUserInfoByUserId(user.getId());

            response.addCookie(new Cookie("X-Api-Key",userInfo.getApiKey()));
            response.addCookie(new Cookie("uuid",String.valueOf(user.getId())));
        
            return "redirect:/";
        }
        model.addAttribute("content", "username or password are not correct");

       	return "login";
      }

    @GetMapping("/login")
    public String loginPage(){
        return "login";
    }

    @GetMapping("/settings")
    public String settings(@CookieValue(name = "X-Api-Key", required = false) String apiKey, Model model){
        UserInfo userInfo = userInfoRepository.findUserInfoByApiKey(apiKey);
        if(null != userInfo){
            model.addAttribute("content", userInfo.getName());
            return "settings";
        }else{
            return "login";
        }
    }

    @GetMapping("/admin")
    public String settings(@CookieValue(name = "uuid", required = false) int uuid){
        User user = userRepository.findAdminUserById(uuid);
        if(null != user){
            return "admin";
        }else{
            return "login";
        }
    }

  
    
}
