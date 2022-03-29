package com.skf.labs.sqliblind;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.beans.factory.annotation.Autowired;


@Controller
public class SqliBlindController {
    @Autowired
    private SqliBlindModel sqliModel;

    @GetMapping("/home/{id}")
    public String home(@PathVariable String id, Model model) {
        List<Page> pages = sqliModel.getPage(id);
        if(pages.size() > 0){
          if(id.equals("1") || id.equals("2") || id.equals("3")){
            model.addAttribute("page", pages.get(0));
          }
          return "index";
        }else{
          return "error";
        }
      }
    
}
