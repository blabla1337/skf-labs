package com.skf.labs.idor;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.HttpStatus;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;


@Controller
public class IdorController {

    @PostMapping("/download")
    public ResponseEntity<Resource> download(@RequestParam(name="pdf_id", required=true) String pdf_id) throws IOException {
        HttpHeaders header;
        if(IdorModel.pdfs.indexOf(Integer.parseInt(pdf_id)) != -1){
            String fileName = pdf_id+".pdf";
            File file = new File(fileName);
            Path path = Paths.get(file.getAbsolutePath());
            ByteArrayResource resource = new ByteArrayResource(Files.readAllBytes(path));
            header = new HttpHeaders();
            header.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename="+fileName);
            return ResponseEntity.ok().headers(header).contentLength(file.length()).contentType(MediaType.parseMediaType("application/octet-stream")).body(resource);
        }else{
            header = new HttpHeaders();
            header.add("Location", "/notfound");    
            return new ResponseEntity<Resource>(header,HttpStatus.FOUND);
        }
       
    }

    @PostMapping("/create")
    public String create(@RequestParam(name="message", required=true) String message, Model model){
        int pdfId = IdorModel.createPdf(message);
        model.addAttribute("content", "Pdf created successfully! ID:"+pdfId);
        return "index";
    }

    @GetMapping("/notfound")
    public String nofound(Model model){
        model.addAttribute("content", "Pdf not found. Try with another id between 1 and 1500.");
        return "index";
    }

    

}

