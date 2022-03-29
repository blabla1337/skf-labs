package com.skf.labs.clientsiderestrictionbypass;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class ClientSideRestrictionBypassController {

    @PostMapping("/verify")
	public String home(@RequestParam(name="number", required=true) String sleepingTime, Model model) {

        try{
            if(Integer.parseInt(sleepingTime) < 7 && Integer.parseInt(sleepingTime) >= 3){
                model.addAttribute("result", "You should sleep more");
            }else if( Integer.parseInt(sleepingTime) >= 7 &&  Integer.parseInt(sleepingTime) <= 9){
                model.addAttribute("result", "You sleep a proper while");
            }else if( Integer.parseInt(sleepingTime) > 9 &&  Integer.parseInt(sleepingTime) <= 13){
                model.addAttribute("result", "You sleep a proper while");
            }else if( Integer.parseInt(sleepingTime) == 2 || ( Integer.parseInt(sleepingTime) > 13 &&  Integer.parseInt(sleepingTime) >24)){
                model.addAttribute("result", "OMG!");
            }
            return "index";
        }catch(java.lang.NumberFormatException e){
            model.addAttribute("result", "That's not possible... HACKER!!");
            return "index";
        }
		
	}

    
}
