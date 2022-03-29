package com.skf.labs.csp;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import javax.servlet.http.HttpServletResponse;


@Controller
public class CspController {
    @PostMapping("/unprotected")
	public String home(@RequestParam(name="no_csp", required=false, defaultValue="World") String xss, Model model) {
		model.addAttribute("xss", xss);
		return "index";
	}

    @PostMapping("/protected")
	public String home(@RequestParam(name="with_csp", required=false, defaultValue="World") String xss, Model model,HttpServletResponse response) {
        response.addHeader("Content-Security-Policy","default-src 'self'");
        response.addHeader("Content-Security-Policy","script-src 'http://127.0.0.1'");
		model.addAttribute("xss", xss);
		return "index";
	}

}
