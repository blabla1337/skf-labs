package com.skf.labs.urlredirection;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class UrlRedirectionController {


    @GetMapping("/")
	public String home(Model model) {
		model.addAttribute("content", "Sorry, this is the old website.");
		return "index";
	}
    
    @GetMapping("/newsite")
	public String newsite(Model model) {
		model.addAttribute("content", "Welcome to the new website!");
		return "index";
	}

    @RequestMapping(
        value = "/redirect",
        method = {
            RequestMethod.GET,
            RequestMethod.POST
        }
    )
	public String redirect(@RequestParam(name="newurl", required=true) String newurl, Model model) {
		return "redirect:"+newurl;
	}
    
}
