package com.skf.labs.lfi3;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URLDecoder;
import java.util.Scanner;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.core.io.ClassPathResource;


@Controller
public class Lfi3Controller {
    
    @PostMapping("/home")
	public String home(@RequestParam(name="filename", required=false, defaultValue="World") String filename, Model model) {
        if(filename.indexOf(".") == -1 && filename.indexOf("/") == -1 && filename.indexOf("\\") == -1){
            filename = URLDecoder.decode(filename);
            try (BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(filename)))){           
                StringBuilder content = new StringBuilder();
                String line;
                while((line = br.readLine())!= null){
                    content.append(line);
                }
                model.addAttribute("read", content.toString());
            }catch(FileNotFoundException e){
                e.printStackTrace();
                model.addAttribute("read","Try harder!");
                return "index";
            }catch(IOException e){
                e.printStackTrace();
                model.addAttribute("read","Try harder!");
                return "index";
            }
         }else{
            model.addAttribute("read","Try harder!");
         }
         return "index";
	}
}
