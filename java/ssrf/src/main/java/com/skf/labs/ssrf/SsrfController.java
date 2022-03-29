package com.skf.labs.ssrf;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.SocketException;
import java.net.URL;

import org.apache.commons.validator.routines.UrlValidator;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;


@Controller
public class SsrfController {
    @PostMapping("/check_existence")
    public String nofound(@RequestParam(name="url", required=true) String url,Model model) {
    String[] schemes = {"http"};
    UrlValidator urlValidator = new UrlValidator(schemes,UrlValidator.ALLOW_LOCAL_URLS);
   
    if(!urlValidator.isValid(url)){
        model.addAttribute("content", "The URL schema is not valid.");    
        return "index";
    }
    try{
        URL u = new URL(url);
        HttpURLConnection con = (HttpURLConnection) u.openConnection();
        con.setRequestMethod("GET");
        con.setConnectTimeout(2000);
        con.setReadTimeout(1000);
        Reader streamReader = null;
        int status = con.getResponseCode();
    }catch(MalformedURLException e){
        e.printStackTrace();
    }catch(IOException e){
        if(e.getMessage().contains("Connection refused")){
            model.addAttribute("content", "Target resource is not reacheable.");     
        }else if(e.getMessage().contains("Read timed out") || e.getMessage().contains("Unexpected end of file from server") || e.getMessage().contains("Invalid argument") ){
            model.addAttribute("content", "Target resource is reacheable!");     
        }else{
            e.printStackTrace();
        }
        return "index";
    }

    model.addAttribute("content", "Webpage found!");     
    return "index";
    }
}
