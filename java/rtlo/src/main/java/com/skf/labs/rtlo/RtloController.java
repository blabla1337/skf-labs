package com.skf.labs.rtlo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class RtloController {
	@PostMapping("/home")
	public String home(@RequestParam(name = "string", required = false, defaultValue = "") String name, Model model) {
		model.addAttribute("rtlo", name);
		return "index";
	}

}
