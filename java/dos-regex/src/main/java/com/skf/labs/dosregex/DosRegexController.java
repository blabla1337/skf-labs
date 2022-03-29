package com.skf.labs.dosregex;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


@Controller
public class DosRegexController {
    @PostMapping("/verify_email")
	public String home(@RequestParam(name="email", required=false, defaultValue="World") String email, Model model) {
        Pattern pattern = Pattern.compile("^([0-9a-zA-Z]([-.\\w]*[0-9a-zA-Z])*@{1}([0-9a-zA-Z][-\\w]*[0-9a-zA-Z]\\.)+[a-zA-Z]{2,9})$", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher(email);
        
        if(matcher.find()){
		    model.addAttribute("result", "Matched!");
        }else{
            model.addAttribute("result", "Not matched!");
        }

		return "index";
	}

    
}
