package com.skf.labs.httpresponsesplitting;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpServletRequest;

@Controller
public class HttpResponseSplittingController {

    @GetMapping("/web")
    public String home(@RequestParam(name = "numero", required = false) Integer numero, Model model,
            HttpServletRequest request) {
        model.addAttribute("numero", numero);
        return "index2";
    }
}
