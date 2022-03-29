package com.skf.labs.sqli;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.beans.factory.annotation.Autowired;


@Controller
public class SqliController {
    @Autowired
    private SqliModel sqliModel;

    @GetMapping("/home/{id}")
    public String home(@PathVariable String id, Model model) {
        List<Page> pages = sqliModel.getPage(id);
        model.addAttribute("page", pages.get(0));
        return "index";
      }
    
}
