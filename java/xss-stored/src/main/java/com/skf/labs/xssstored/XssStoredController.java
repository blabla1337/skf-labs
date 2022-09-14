
package com.skf.labs.xssstored;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import org.springframework.web.bind.annotation.PathVariable;

import com.skf.labs.xssstored.Page;
import com.skf.labs.xssstored.XssStoredModel;

import org.springframework.beans.factory.annotation.Autowired;

@Controller
public class XssStoredController {
    @Autowired
    private XssStoredModel xssModel;

    @GetMapping("/home/{id}")
    public String home(@PathVariable String id, Model model) {
        List<Page> pages = xssModel.getPage(id);
        model.addAttribute("page", pages.get(0));
        return "index";
    }

    @PostMapping("/update")
	public String update(@RequestParam(name="pageId", required=true) int pageId,
                        @RequestParam(name="title", required=true) String title,
                        @RequestParam(name="content", required=true) String content) {
    Page page = new Page(pageId, title, content);
    xssModel.updatePage(page);
        return "redirect:/home/"+pageId;
    }



    
}
