package com.skf.labs.xss;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class XssController {

	@PostMapping("/home")
	public String home(@RequestParam(name="string", required=false, defaultValue="World") String name, Model model) {
		model.addAttribute("xss", name);
		return "index";
	}

}