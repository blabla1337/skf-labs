package com.skf.labs.cssi;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.ui.Model;


@Controller
public class CssiController {
    @PostMapping("/home")
	public String home(@RequestParam(name="inj_text", required=true) String inj_text,Model model) {
        model.addAttribute("content", inj_text);
        return "index";
    }
}
